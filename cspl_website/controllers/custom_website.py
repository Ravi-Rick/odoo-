from datetime import datetime
from odoo import http
from odoo.http import request
from odoo import http
from .functions import CsplWebsiteFunctions
from .sms import SMSApi
import random
import string



class CustomWebsite(http.Controller):
    @http.route('/api/banners/', type='json', auth='none', csrf=False, cors='*')
    def banners(self,lang='en_US' ,uid=None):
        data = request.env["cspl_eccomerce_api.advert"].sudo().search([],limit=1)
        
        banner = [
            {
                "image":f"/web/image/cspl_website.cspl_website/{i.id}/image"
                ,"mobile_image":f"/web/image/cspl_website.cspl_website/{i.id}/mobile_image"
                ,"title":i.name
                ,"subtitle":i.description
                ,"link":i.link
            }for i in request.env["cspl_website.cspl_website"].sudo().search([('is_active','=',True)])]
        carousel = [
            {
                "images":f"/web/image?model=res.company.carousel&id={i.id}&field=image",
                "link":i.link,
                "description":i.description,
                } for i in data.carousel_ids
        ]
        second_carousel = [
            {
                "images":f"/web/image?model=res.company.carousel&id={i.id}&field=image",
                "link":i.link,
                "description":i.description,
                } for i in data.second_carousel_ids
        ]
        return {
            
            'banners':banner,
            'carousel':carousel,
            'second_carousel':second_carousel,
            'category':{
                "title": data.category_image_title,
                "image": f"/web/image?model=cspl_eccomerce_api.advert&id={data.id}&field=category_image",
                "link": data.category_image_url
                },
          
            
            'advert_1':{
                "first":{
                    'image':f"/web/image?model=cspl_eccomerce_api.advert&id={data.id}&field=multi_ads_image_1",
                    'url':data.multi_ads_image_1_url
                },
                "second":{
                    'image':f"/web/image?model=cspl_eccomerce_api.advert&id={data.id}&field=multi_ads_image_2",
                    'url':data. multi_ads_image_2_url
                },
                } if data.multi_ads_active else {},
            'advert_2':{
                'image':f"/web/image?model=cspl_eccomerce_api.advert&id={data.id}&field=single_ad_image",
                'url':data.single_ad_image_url
                } if data. single_ad_active else {},
            
            'newsletter':{
                'image':f"/web/image?model=cspl_eccomerce_api.advert&id={data.id}&field=newsletter_image",
                },
        }


    @http.route('/api/features/',type='json',auth='public',csrf=False,cors='*')
    def features(self,**kwargs):
        try:
            Feature = request.env['cspl_website.feature']
            features =Feature.sudo().search([])
            data=[]
            for feature in features:
                feature_data={
                    'text':feature.text,
                    'heading':feature.heading,
                    "image":f"/web/image?model=cspl_website.feature&id={feature.id}&field=image",
                }
                data.append(feature_data)
            return{'sucsees':True,'feature_data':data}
        except Exception as e:
            return{'sucsees':False,'error':str(e)}
        
        
    @http.route('/api/sub_to_newsletter', type='json', auth='none',csrf=False, cors='*')
    def sub_to_newsletter(self,email=None, **kw):
        mailing_list = request.env['mailing.list'].sudo().search([("name","ilike","Newsletter")],limit=1)
        if mailing_list:
            existing_contact = request.env['mailing.contact'].sudo().search([('email', '=', email)], limit=1)
            if existing_contact:
                if existing_contact in mailing_list.contact_ids:
                    return {'success': True,'exist':True, 'message': 'Email already subscribed to this newsletter'}
                else:
                    mailing_list.contact_ids = [(4, existing_contact.id)]
                    return {'success': True,'exist':False, 'message': 'Existing contact added to the newsletter'}
            else:
                contact = request.env['mailing.contact'].sudo().create({'email': email})
                mailing_list.contact_ids = [(4, contact.id)]
                return {'success': True,'exist':False, 'message': 'New contact subscribed to the newsletter'}
        else:
            return {'success': False, 'error': 'Newsletter not found'}
