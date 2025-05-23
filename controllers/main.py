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
        raw_values = {
            'name': name,
            'list_price': price,
            'barcode': barcode_value,
            'description': description.strip(),
            'creator_id': user.id,
            'title': post.get('title'),  
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
            'dimensions': post.get('dimensions'),
            'weight': post.get('weight'),
            'release_date': post.get('release_date'),
            'feature': post.get('feature'),
        }

        # Call custom handler
        product = request.env['product.template'].with_context({}).sudo().manual_product_data_handler(raw_values, user.id)

        # Reward points
        user.sudo().write({
            'creation_points': user.creation_points + 10
        })

        # ✅ Render success page with product info
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
