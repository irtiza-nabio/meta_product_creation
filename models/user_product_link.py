from odoo import models, fields

class ResUsers(models.Model):
    _inherit = 'res.users'

    product_ids = fields.One2many('product.template', 'creator_id', string='Created Products')
    creation_points = fields.Char(string='Product Creation Points', default=0)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    creator_id = fields.Many2one('res.users', string='Created By')
