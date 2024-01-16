# -*- coding: utf-8 -*-

from odoo import models, fields, api


# class doctor(models.Model):
#     _name = 'doctor.doctor'
#     _description = 'doctor.doctor'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100


class doctor(models.Model):
    _name= "doctor"
    _description= "doctor_Records"
  

    name = fields.Char(string='name')
    # gender = fields.Selection([{'male':'male'},{'female':'female'},{'others':'others'}],string='gender')
    gender = fields.Selection([
    ('male', 'Male'),
    ('female', 'Female'),
    ('others', 'Others')
], string='Gender')

    ref = fields.Char(string="Reference",required=True)
    description = fields.Text(translate=True)
    image = fields.Binary(string="image")
    # active = fields.Boolean(default=True) 
    