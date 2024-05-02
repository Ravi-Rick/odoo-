from odoo import models, fields, api
from odoo import fields



class ResPartner(models.Model):
    _inherit = 'res.partner'

    auth_token = fields.Char(string='auth_token')
    otp = fields.Integer(string='OTP',default=000000)
    otp_generated_at = fields.Datetime(string='OTP Generated At', default=fields.Datetime.now)
    
    @api.onchange('otp')
    def _onchange_otp(self):
        self.otp_generated_at = fields.Datetime.now
