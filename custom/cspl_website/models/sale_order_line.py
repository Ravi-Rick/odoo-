from odoo import fields, models



class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    product_uom_category_id = fields.Many2one('uom.category')
    product_uom = fields.Many2one(
        comodel_name='uom.uom',
        string="Unit of Measure",
        ondelete='restrict',
        domain="[('category_id', '=', product_uom_category_id)]"
    )

    