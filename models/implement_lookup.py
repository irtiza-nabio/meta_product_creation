from odoo import models, fields

class ResUsers(models.Model):
    _inherit = 'res.users'

    creation_points = fields.Integer(string="Product Creation Points", default=0)
    product_ids = fields.One2many('product.template', 'create_uid', string="Created Products")


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    creator_id = fields.Many2one('res.users', string='Created By')
    creation_date = fields.Datetime(string='Creation Date', default=fields.Datetime.now)

    product_create_source = fields.Selection([
        ('scanned', 'Scanned'),
        ('manual', 'Manual'),
    ], string="Source")

    product_upc = fields.Char("UPC")
    product_category = fields.Char("Category")
    product_title = fields.Char("Title")
    product_mpn = fields.Char("MPN")
    product_model = fields.Char("Model")
    product_manufacturer = fields.Char("Manufacturer")
    product_brand = fields.Char("Brand")
    product_age_group = fields.Char("Age Group")
    product_color = fields.Char("Color")
    product_multipack = fields.Char("Multipack")
    product_size = fields.Char("Size")
    product_length = fields.Char("Length")
    product_width = fields.Char("Width")
    product_height = fields.Char("Height")
    product_weight = fields.Char("Weight")
    product_release_date = fields.Datetime("Release Date")  
    product_description = fields.Text("Description")  
    product_feature = fields.Text("Feature")  
    product_image_urls = fields.Text("Image URLs") 
