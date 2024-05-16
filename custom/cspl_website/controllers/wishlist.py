from odoo import http
from odoo.http import request
from odoo import http



class Wishlist(http.Controller):
    @http.route('/api/wishlist/get/', auth='public', type='json', csrf=False, cors='*')
    def get_wishlist(self, user_id=None, login_token=None, language='en_US'):
        user = request.env['res.partner'].sudo().search([('id', '=', user_id), ('auth_token', '=', login_token)])
        
        if not user:
            return {'error': 'User not found'}
        
        try:
            product_list = []

            website_id = request.env.ref('website.default_website').id

            wishlist = request.env['product.wishlist'].sudo().search([
                ("partner_id", "=", user_id),
                ("website_id", "=", website_id),
            ])
            
            for data in wishlist:
                product = data.product_id
                
                product_list.append({
                    "wishlist_id": wishlist.id,
                    "name": product.name,
                    "slug": product.slug,
                    "brand": product.brand_id.name,
                    "category": product.categ_id.name,
                    "sales_price": product.list_price,
                    "discount_price": product.discount_price,
                    "discount_percent": product.discount_percent,
                    "image": f"/web/image?model=product.template&id={product.id}&field=image_512",
                    "in_stock": product.in_stock,
                })

            return product_list
        
        except Exception as e:
            return {"error": e}

    @http.route('/api/wishlist/add/', auth='public', type='json', csrf=False, cors='*')
    def add_item_to_wishlist(self, product_id, user_id, login_token):
        user = request.env['res.partner'].sudo().search([('id', '=', user_id), ('auth_token', '=', login_token)])
        
        if not user:
            return {'error': 'User not found'}

        website_id = request.env.ref('website.default_website').id
        
        is_in_wishlist = request.env['product.wishlist'].sudo().search([
            ("product_id", "=", product_id),
            ("partner_id", "=", user_id),
            ("website_id", "=", website_id),
        ])

        if is_in_wishlist:
            return {'error': 'Product already in wishlist'}
        
        wish = request.env['product.wishlist'].sudo().create({
            'partner_id': user.id,
            'product_id': product_id,
            'website_id': website_id,
        })

        if not wish:
            return {'error': 'Something went wrong'}

        return {'message': 'Product added in the wishlist'}

    @http.route('/api/wishlist/remove/', auth='public', type='json', csrf=False, cors='*')
    def remove_item_from_wishlist(self, product_id, user_id, login_token):
        user = request.env['res.partner'].sudo().search([('id', '=', user_id), ('auth_token', '=', login_token)])
        
        if not user:
            return {'error': 'User not found'}

        website_id = request.env.ref('website.default_website').id
        
        is_in_wishlist = request.env['product.wishlist'].sudo().search([
            ("product_id", "=", product_id),
            ("partner_id", "=", user_id),
            ("website_id", "=", website_id),
        ])

        if not is_in_wishlist:
            return {'error': 'Product not in wishlist'}
        
        is_in_wishlist.sudo().unlink()

        return {'message': 'Product removed from the wishlist'}
