from odoo import models, fields, api, exceptions
class cspl_eccomerce_api(models.Model):
    _name = 'cspl_eccomerce_api.advert'
    _description = 'CSPL Eccomerce Api Adverts'
    _rec_name = "custom_name"
    
    custom_name = fields.Char(string="Custom Name",required=True)
    
    multi_ads_active = fields.Boolean(string='section1 multi ads ',)

    multi_ads_image_1_title = fields.Char(string='image4_title', translate=True)
    multi_ads_image_1 = fields.Binary(string="section one first Image")
    multi_ads_image_1_url = fields.Char(string='image1_url',)

    multi_ads_image_2_title = fields.Char(string='image4_title', translate=True)
    multi_ads_image_2 = fields.Binary(string="section one second Image") 
    multi_ads_image_2_url = fields.Char(string='image2_url',)
    
    # single ad
    single_ad_active = fields.Boolean(string='section2 single ad',)
    single_ad_image = fields.Binary(string="section two Image")
    single_ad_image_url = fields.Char(string='image2_url',)
    
    # category section 
    category_image = fields.Binary(string="section three Image")
    category_image_url = fields.Char(string='category Redirect',)
    category_image_title = fields.Char(string='Title', translate=True)

    # countdown section
    countdown_active = fields.Boolean(string='section4',)
    countdown_image = fields.Binary(string="section four Image")
    countdown_image_url = fields.Char(string='image4_url',)
    countdown_image_title = fields.Char(string='image4_title', translate=True)
    countdown_image_description = fields.Char(string='image4_description',translate=True)
    
    #newsletter section
    newsletter_image = fields.Binary(string="newsletter Image")
    carousel_ids = fields.One2many('res.company.logoss', 'company_id', string='carousel')
    second_carousel_ids = fields.One2many('res.company.carousel', 'parent_id', string='carousel 2')

    @api.onchange('countdown_image_url', 'multi_ads_image_1_url', 'multi_ads_image_2_url', 'single_ad_image_url',
                  'category_image_url')
    def onchange_varify_url(self):
        for record in self:
            if record.countdown_image_url and not record.countdown_image_url.startswith('/'):
                warning_message = "The countdown redirect url must start with '/' character."
                raise exceptions.ValidationError(warning_message)
            if record.multi_ads_image_1_url and not record.multi_ads_image_1_url.startswith('/'):
                warning_message = "The advert section one redirect url must start with '/' character."
                raise exceptions.ValidationError(warning_message)
            if record.multi_ads_image_2_url and not record.multi_ads_image_2_url.startswith('/'):
                warning_message = "The advert section one redirect url must start with '/' character."
                raise exceptions.ValidationError(warning_message)
            if record.single_ad_image_url and not record.single_ad_image_url.startswith('/'):
                warning_message = "The advert section two redirect url must start with '/' character."
                raise exceptions.ValidationError(warning_message)
            if record.category_image_url and not record.category_image_url.startswith('/'):
                warning_message = "The category advert redirect url must start with '/' character."
                raise exceptions.ValidationError(warning_message)

    # temp_field = fields.Binary("WebP Image", compute='convert_image_to_webp', store=True)
class ResCompanyLogos(models.Model):
    _name = "res.company.logoss"
    company_id = fields.Many2one('cspl_eccomerce_api.advert', string='company', required=True, ondelete='cascade', index=True)
    image = fields.Image(string="image", attachment=True)
    description = fields.Text(string='description')
    link = fields.Char(string='link')
    
    
    
class ResCompanyCarousel(models.Model):
    _name = "res.company.carousel"
    parent_id = fields.Many2one('cspl_eccomerce_api.advert', string='company', required=True, ondelete='cascade', index=True)
    image = fields.Image(string="image", attachment=True)
    description = fields.Text(string='description')
    link = fields.Char(string='link')
    
    
    