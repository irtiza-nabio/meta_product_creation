from odoo import models, fields

class ResUsers(models.Model):
    _inherit = 'res.users'

    # Relationship to track created products
    product_ids = fields.One2many('product.template', 'creator_id', string='Created Products')

    # Track product creation points
    creation_points = fields.Integer(string='Product Creation Points', default=0)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # Relationship to the user who created the product
    creator_id = fields.Many2one('res.users', string='Created By')
