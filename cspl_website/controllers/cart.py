from datetime import datetime
from odoo import http
from odoo.http import request
from odoo import http
from .functions import CsplWebsiteFunctions
from .sms import SMSApi
import random
import string


class CartApi(http.Controller):
        
    http.route('api/getcart',type='json',auth='public',csrf=False)
    def getapi(self,user_id=None,login_token=None,languages='en_US'):
        user = request.env['res.partner'].sudo.search([('id','=',user_id),('auth_token','=',login_token)])
        if not user:
            return {'error':'User not found'}
        try:
            product_list =[]
            
            website_id = request.env.ref['website.default_website'].id
            
            cart = request.env['sale.order'].sudo().search([
                ('partner_id','=',user.id),
                (website_id, '=',website_id),
                ('state','=','draft')
            ],limit=1)
            
            if cart:
                for data in cart.order_line:
                    product = data.product_id
                    
                    product_list.append({
                        'line_id':data.line_id,
                        'name':data.name,
                        'slug':data.slug,
                        'brand':data.brand,
                        'category':data.category,
                        'sale_price':data.sale_price,
                        'discount_price':data.discount_price,
                        'discount_percent':data.discount_percent,
                        'image':f"web/image?model=product.template&id={product.id}&field=image",
                        'in_stock':data.in_stock,
                    })
                    
                return{
                    "cart_id":cart.id,
                    "products": product_list
                }
            else:
                return "Cart is empty"
        except Exception as e:
            return {'error':str(e)}
        
        


    @http.route('/api/addtocart', type='json', auth='public', csrf=False)
    def add_to_cart(self, user_id=None, login_token=None, product=None):
        try:
            user = request.env['res.partner'].sudo().search([('id','=',user_id),('auth_token','=',login_token)])
            if not user:
                return {'error':'User not found'}
            if not product:
                return {'error':'Products not found'}
            
            cart = request.env['sale.order'].sudo().create({
                'partner_id': user.id,
                'website_id': request.env.ref('website.default_website').id,
            })
            
            for product_id, quantity in product.items():
                product = request.env['product.product'].sudo().browse(int(product_id))
                if product:
                    request.env['sale.order.line'].sudo().create({
                        'order_id': cart.id,
                        'product_id': product.id,
                        'product_uom_qty': quantity,
                        'price_unit': product.list_price,
                        'name': product.name,
                        'discount_percent':product.discount_percent,
                        'discount_price': product.discount_price,
                        'image':f"web/image?model=product.product&id={product.id}&field=image"
                    })
            return {'message': 'Cart created successfully'}
        except Exception as e:
            return {'error': str(e)}
        
        
        
    @http.route('api/removeToCart',type='json',auth='public',csrf=False)
    def remove_to_cart(self,user_id=None,login_token=None,product_id=None):
        try:
            user = request.env['res.partner'].sudo().search([('id','=',user_id),('auth_token','=',login_token)])
            if not user:
                return {'error':'User not found'}
            cart = request.env['sail.order'].sudo().search([('partner_id','=',user_id),('state','=','draft')],limit=1)
            
            if not cart:
                return {'error':'Cart not found'}
            
            product = request.env['product.product'].sudo().browse(int(product_id))
            
            if not product:
                return {'error':'Product not found'}
            line = request.env['sale.order.line'].sudo().search([('order_id', cart.id),('product_id', product.id)],limit=1)
            
            if not line:
                return {'error':'prduct not in cart'}
            line.unlink()
            return {'message':'product removed from cart successfully'}
        
        except Exception as e:
            return {'error':str(e)}

            
        
            
        