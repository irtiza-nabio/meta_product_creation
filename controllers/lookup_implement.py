from odoo import http
from odoo.http import request
import base64

class ProductUserTrackingController(http.Controller):

    @http.route('/user/product/create', type='http', auth="user", website=True, csrf=True)
    def create_product_form(self, **post):
        return request.render('meta_product_creation.product_create_form_template', {})

    @http.route('/user/product/submit', type='http', auth="user", website=True, methods=["POST"], csrf=True)
    def product_submit(self, **post):
        user = request.env.user
        name = post.get('name', '').strip()
        price = post.get('price')
        description = post.get('description', '')
        barcode = post.get('barcode')
        image_file = request.httprequest.files.get('image')

        # Validate name and price
        if not name or not price:
            return self.render_product_form_with_error(
                'Product name and price are required.',
                name, price, description, barcode
            )

        # Ensure name is not just whitespace
        if name.strip() == '':
            return self.render_product_form_with_error(
                'Product name cannot be empty or just spaces.',
                name, price, description, barcode
            )

        # Convert price to float
        try:
            price = float(price)
        except ValueError:
            return self.render_product_form_with_error(
                'Price must be a number.',
                name, price, description, barcode
            )

        # Convert barcode to int
        try:
            barcode_value = int(float(barcode)) if barcode else 0
        except (ValueError, TypeError):
            return self.render_product_form_with_error(
                'Barcode must be a number.',
                name, price, description, barcode
            )

        # Prepare raw values to be passed to the model
        raw_data = {
            'products': [
                {
                    'title': post.get('title'),
                    'description': post.get('description'),
                    'upc': post.get('upc'),
                    'category': post.get('category'),
                    'mpn': post.get('mpn'),
                    'model': post.get('model'),
                    'manufacturer': post.get('manufacturer'),
                    'brand': post.get('brand'),
                    'age_group': post.get('age_group'),
                    'color': post.get('color'),
                    'multipack': post.get('multipack'),
                    'size': post.get('size'),
                    'length': post.get('length'),
                    'width': post.get('width'),
                    'height': post.get('height'),
                    'weight': post.get('weight'),
                    'release_date': post.get('release_date'),
                    'feature': post.get('feature'),
                    # Add any other necessary fields here
                }
            ]
        }

        # Create a new product template
        product = request.env['product.template'].sudo().create({
            'name': name,
            'list_price': price,
            'barcode': barcode_value,
            'creator_id': user.id,
        })

        # Handle image upload if available
        if image_file:
            image_data = image_file.read()  # Read the image file
            image_base64 = base64.b64encode(image_data)  # Convert to base64
            image_attachment = request.env['ir.attachment'].sudo().create({
                'name': f"{name}_image.jpg",  # You can change the file extension based on the uploaded file type
                'type': 'binary',
                'datas': image_base64,
                'res_model': 'product.template',
                'res_id': product.id,
                'mimetype': 'image/jpeg',  # Adjust based on the image type
            })
            product.write({
                'image_1920': image_attachment.datas  # Store image in the product template
            })

        # Now update the product using the barcode lookup method
        request.env['product.template'].sudo()._update_product_by_barcodelookup(product, raw_data)

        # Add points to the user for product creation
        user.sudo().write({
            'creation_points': user.creation_points + 10
        })

        # Render success page with product info
        return request.render('meta_product_creation.product_create_success', {
            'product': product,
            'reward_points': user.creation_points,
            'creation_date': product.create_date.strftime('%Y-%m-%d %H:%M:%S') if product.create_date else ''
        })

    def render_product_form_with_error(self, error_message, name, price, description, barcode):
        return request.render('meta_product_creation.product_create_form_template', {
            'error_message': error_message,
            'name': name,
            'price': price,
            'description': description,
            'barcode': barcode
        })

    @http.route('/user/products', type='http', auth="user", website=True)
    def view_user_products(self, **kwargs):
        user = request.env.user
        products = user.product_ids
        points = user.creation_points

        return request.render('meta_product_creation.user_product_list_template', {
            'products': products,
            'page_name': 'products',
            'points': points
        })
