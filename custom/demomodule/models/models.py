# -*- coding: utf-8 -*-

from odoo import models, fields, api


class demomodule(models.Model):
    _name = 'demomodule.demomodule'
    _inherit= 'mail.thread'
    _description = 'demomodule.demomodule'
    

    name = fields.Char(tarcking=True)
    value = fields.Integer(tracking=True)
    value2 = fields.Float(compute="_value_pc", store=True)
    description = fields.Text(translate=True)
    image = fields.Binary(string="image")
    doctor_id = fields.Many2one('doctor',string="Doctor")
    active = fields.Boolean(string="active",default=True)
    color =  fields.Integer(string="color")
    color2 = fields.Integer(string="color") 
    
    tag_ids = fields.Many2many('res.partner',string="Tags")
    pharmacy_line_ids = fields.One2many('appointment.pharmacy.line','appointment_id',string='pharmacy line')
    

   
    
    

    @api.depends('value')
    def _value_pc(self):
        for record in self:
            record.value2 = float(record.value) / 100   
    
    @api.model
    def test_corn_job(self):
        print('..............................ABCD--------------------------------')
            
            


class ApppointPhramacyLine(models.Model):
    _name = 'appointment.pharmacy.line'
    _description = 'appointment pharmacy line'

    product_id=fields.Many2one('product.product')
    price_unit=fields.Float(string="Price")
    qty=fields.Integer(string="Quantity")
    appointment_id=fields.Many2one('demomodule.demomodule',string='Appointment')
    image = fields.Binary(related='product_id.image_1920',string='Image',readonly= True)








class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_published = fields.Boolean(string='Is Published')
    
    
    


class ProductProduct(models.Model):
    _inherit = 'product.product'

    # description = fields.Char(string="sale",copy=False)
    description_sale = fields.Char(string="sale",copy=False)
    
    description= fields.Char(string="description",copy=False)
    
    
    
 


# class CustomHtmlWidget(fields.Html):

#     def __init__(self, *args, **kwargs):
#         super(CustomHtmlWidget, self).__init__(*args, **kwargs)
#         self.options['toolbar'] = [
#             ['style', ['bold', 'italic']],
#             ['insert', ['link']],
#             ['para', ['ul', 'ol']],
#         ]

# class ProductTemplate(models.Model):
#     _inherit = 'product.template'

#     description = fields.Html('Custom Description', translate=True, widget=CustomHtmlWidget,no_table=True)



# class ResPartner(models.Model):
#     _inherit = 'res.partner'

#     is_published = fields.Boolean(string='Is Published')

#     def button_do_something(self):  
#         self.write({'is_published': True})

#         if self.is_published:
           
#             print("Hello World!")
#         return {'type': 'ir.actions.act_window_close'}





class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_published = fields.Boolean(string='Is Published')

    def button_do_something(self):
        # Update is_published field
        self.write({'is_published': True})

        # Send an email
        try:
            template_id = self.env.ref('demomodule.mail_template_contact_person_mail')
            template_id.send_mail(self.id, force_send=True)
            print("email sent")
        except Exception as e:
            print(e)
            return {'warning': {'title': 'Error', 'message': str(e)}}

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Congratulations!',
                'message': 'The email has been sent successfully.',
                'sticky': False,
            }
        }
        
    
# class SheduleActons(models.Model):
#     _inherit = "demomodule.demomodule"
    
#     @api.model
#     def test_corn_job(self):
#         print("------------------------ABCD..............................")
#         print("------------------------ABCD..............................")
#         print("------------------------ABCD..............................")
#         print("------------------------ABCD..............................")
#         print("------------------------ABCD..............................")
#         print("------------------------ABCD..............................")
#         print("------------------------ABCD..............................")
#         print("------------------------ABCD..............................")
#         print("------------------------ABCD..............................")
        








            

     









    
    

     

