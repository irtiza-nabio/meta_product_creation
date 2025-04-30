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
        name = post.get('name')
        price = post.get('price')
        description = post.get('description')
        image_file = request.httprequest.files.get('image')

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
                'error_message': 'Price must be a number',
                'name': name,
                'description': description
            })
        
        values = {
            'name': name.strip(),
            'list_price': price,
            'description': description.strip() if description else '',
            'creator_id': user.id    
        }

        if image_file and image_file.filename:
            image_data = image_file.read()
            if image_data:
                values['image_1920'] = base64.b64encode(image_data)

        product = request.env['product.template'].sudo().create(values)

        # user.sudo().write({
        #     'creation_points': user.creation_points + 10
        # })

        return request.render('meta_product_creation.product_create_success', {
            'product': product,
            # 'reward_points': user.creation_points
        })

    # @http.route('/user/products', type='http', auth="user", website=True)
    # def view_user_products(self, **kwargs):
    #     user = request.env.user
    #     products = user.product_ids
    #     return request.render('meta_product_creation.user_product_list_template', {
    #         'products': products,
    #         'points': user.creation_points
    #     })

 
