from odoo import models, fields
from odoo import fields



class cspl_website(models.Model):
    _name = 'cspl_website.cspl_website'
    _description = 'cspl_website.cspl_website'

    name = fields.Char("Name",required=True)
    image = fields.Binary("Banner")
    description = fields.Char("Description")
    mobile_image = fields.Binary("Banner Mobile")
    is_active = fields.Boolean("Active",default=False)
    link = fields.Char("Link")


class FeaturePlatform(models.Model):
    _name = 'cspl_website.feature'
    _description = 'cspl_website.feature'
    
    text = fields.Char("Text")
    heading = fields.Char("Heading")
    image = fields.Binary("Image")
