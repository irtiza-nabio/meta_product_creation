from odoo import http, fields, models
from odoo.http import request
import base64

class ProductDescription(models.Model):
    _inherit = 'product.template'

    product_description = fields.Char(string="Description")



class ProductCreateController(http.Controller):

    @http.route('/product/add', type='http', auth="public", website=True, csrf=True)
    def create_product(self, **post):
        """Render the product creation form"""
        return request.render('meta_product_creation.product_create_form_template', {})

    @http.route('/product/submit', type='http', auth="public", website=True, methods=["POST"], csrf=True)
    def submit_product(self, **post):
        """Process the form submission and create a new product"""
        name = post.get('name')
        price = post.get('price')
        description = post.get('description')
        image_file = request.httprequest.files.get('image')

        # Safety check: Ensure name and price are provided
        if not name or not price:
            return request.render('meta_product_creation.product_create_form_template', {
                'error_message': 'Product name and price are required.',
                'name': name,
                'price': price,
                'description': description
            })

        try:
            price = float(price)
        except ValueError:
            return request.render('meta_product_creation.product_create_form_template', {
                'error_message': 'Price must be a valid number.',
                'name': name,
                'description': description
            })

        # Prepare values for the new product
        values = {
            'name': name.strip(),
            'list_price': price,
            'description': description.strip() if description else '',
        }

        # Process the image if provided
        if image_file and image_file.filename:
            image_data = image_file.read()
            if image_data:
                values['image_1920'] = base64.b64encode(image_data)

        # Create the new product template
        product = request.env['product.template'].sudo().create(values)

        # Render success page
        return request.render('meta_product_creation.product_create_success', {
            'product': product,
        })
