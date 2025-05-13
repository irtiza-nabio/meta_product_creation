from odoo import models, fields, api

class ResUsers(models.Model):
    _inherit = 'res.users'

    product_ids = fields.One2many('product.template', 'creator_id', string='Created Products')
    creation_points = fields.Integer(string='Product Creation Points', default=0)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    creator_id = fields.Many2one('res.users', string='Created By')
    creation_date = fields.Datetime(string='Creation Date', default=fields.Datetime.now)

    title = fields.Char("Title")
    upc = fields.Char("UPC")
    category = fields.Char("Category")
    mpn = fields.Char("MPN")
    model = fields.Char("Model")
    manufacturer = fields.Char("Manufacturer")
    brand = fields.Char("Brand")
    age_group = fields.Char("Age Group")
    color = fields.Char("Color")
    multipack = fields.Char("Multipack")
    size = fields.Char("Size")
    dimensions = fields.Char("Dimensions")
    weight = fields.Char("Weight")
    release_date = fields.Char("Release Date")
    feature = fields.Text("Feature")

    @api.model
    def manual_product_data_handler(self, raw_values, user_id):
        """
        Handle manual input: update existing product by barcode or create a new one.
        """
        barcode = str(raw_values.get('barcode')) if raw_values.get('barcode') else None
        
        # Attempt to find an existing product by barcode
        product = self.search([('barcode', '=', barcode)], limit=1) if barcode else None

        values = {
            'name': raw_values.get('name'),
            'list_price': float(raw_values.get('price', 0)),
            'barcode': barcode,
            'description': raw_values.get('description'),
            'creator_id': user_id,
            'title': raw_values.get('title'),
            'upc': raw_values.get('upc'),
            'category': raw_values.get('category'),
            'mpn': raw_values.get('mpn'),
            'model': raw_values.get('model'),
            'manufacturer': raw_values.get('manufacturer'),
            'brand': raw_values.get('brand'),
            'age_group': raw_values.get('age_group'),
            'color': raw_values.get('color'),
            'multipack': raw_values.get('multipack'),
            'size': raw_values.get('size'),
            'dimensions': raw_values.get('dimensions'),
            'weight': raw_values.get('weight'),
            'release_date': raw_values.get('release_date'),
            'feature': raw_values.get('feature'),
        }

        if product:
            product.write(values)
        else:
            product = self.create(values)

        return product
