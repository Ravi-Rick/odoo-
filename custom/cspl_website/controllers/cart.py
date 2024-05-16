from odoo import http
from odoo.http import request
from odoo import http



class Cart(http.Controller):
    # @http.route('/api/cart/get/', auth='public', type='json', csrf=False, cors='*')
    # def get_cart(self, user_id=None, login_token=None, language='en_US'):
    #     user = request.env['res.partner'].sudo().search([('id', '=', user_id), ('auth_token', '=', login_token)])
        
    #     if not user:
    #         return {'error': 'User not found'}
        
    #     try:
    #         product_list = []

    #         website_id = request.env.ref('website.default_website').id
            
    #         cart = request.env['sale.order'].sudo().search([
    #             ('partner_id', '=', user.id),
    #             ("website_id", "=", website_id),
    #             ('state', '=', 'draft')
    #         ], limit=1)

    #         if cart:
    #             if not cart.order_line:
    #                 return {"message": "Cart is empty"}

    #             for data in cart.order_line:
    #                 product = data.product_id

    #                 product_template_id = data.product_template_id.id

    #                 in_wishlist = True

    #                 wishlist = request.env['product.wishlist'].sudo().search([
    #                     ("website_id", "=", website_id),
    #                     ("partner_id", "=", user_id),
    #                     ("product_id", "=", product_template_id),
    #                 ])

    #                 if not wishlist:
    #                     in_wishlist = False

    #                 uom_info = {}

    #                 if (data.pricelist_item_id.id == 0) or (data.pricelist_item_id.id == False):
    #                     uom_info["uom_category_id"] = product.uom_category_id.id
    #                     uom_info["uom_id"] = product.uom_id.id
    #                     uom_info["uom"] = product.uom_id.name
    #                     uom_info["uom_description"] = ""
    #                     uom_info["uom_type"] = product.uom_id.uom_type
    #                     uom_info["sales_price"] = product.list_price
    #                     uom_info["discount_price"] = product.discount_price
    #                     uom_info["discount_percent"] = product.discount_percent
    #                     uom_info["unit_price"] = 0.0
    #                     uom_info["currency"] = product.currency_id.name

    #                 else:
    #                     uom_info["uom_category_id"] = data.product_uom_category_id.id
    #                     uom_info["uom_id"] = data.product_uom.id
    #                     uom_info["uom"] = data.product_uom.name
    #                     uom_info["uom_description"] = data.pricelist_item_id.uom_description if data.pricelist_item_id.uom_description else ""
    #                     uom_info["uom_type"] = data.product_uom.uom_type
    #                     uom_info["sales_price"] = data.pricelist_item_id.fixed_price
    #                     uom_info["discount_price"] = data.pricelist_item_id.discount_price
    #                     uom_info["discount_percent"] = data.pricelist_item_id.discount_percent
    #                     uom_info["unit_price"] = data.pricelist_item_id.unit_price
    #                     uom_info["currency"] = data.pricelist_item_id.currency_id.name
                
    #                 product_list.append({
    #                     "line_id": data.id,
    #                     "product_template_id": product_template_id,
    #                     "product_variant_id": product.id,
    #                     "name": product.name,
    #                     "slug": product.slug,
    #                     "brand": product.brand_id.name if product.brand_id.name else "",
    #                     "category": product.categ_id.name if product.categ_id.name else "",
    #                     "image": f"/web/image?model=product.template&id={product_template_id}&field=image_512",
    #                     "uom_info": uom_info,
    #                     "product_uom_quantity": data.product_uom_qty,
    #                     "in_stock": product.in_stock,
    #                     "in_wishlist": in_wishlist,
    #                 })

    #             return {
    #                 "cart_id": cart.id,
    #                 "subtotal": "",
    #                 "tax_total": "",
    #                 "final_total": "",
    #                 "products": product_list
    #             }

    #         else:
    #             return {"message": "Cart is empty"}
        
    #     except Exception as e:
    #         return {"error": e}
    
    
    @http.route('/api/cart/get/', auth='public', type='json', csrf=False, cors='*')
    def get_cart(self, user_id=None, login_token=None, language='en_US'):
        user = request.env['res.partner'].sudo().search([('id', '=', user_id), ('auth_token', '=', login_token)])
        
        if not user:
            return {'error': 'User not found'}
        
        try:
            product_list = []

            website_id = request.env.ref('website.default_website').id
            
            cart = request.env['sale.order'].sudo().search([
                ('partner_id', '=', user.id),
                ("website_id", "=", website_id),
                ('state', '=', 'draft')
            ], limit=1)

            if cart:
                if not cart.order_line:
                    return {"message": "Cart is empty"}

                subtotal = 0.0
                tax_total = 0.0
                final_total = 0.0

                for data in cart.order_line:
                    product = data.product_id

                    product_template_id = data.product_template_id.id

                    in_wishlist = True

                    wishlist = request.env['product.wishlist'].sudo().search([
                        ("website_id", "=", website_id),
                        ("partner_id", "=", user_id),
                        ("product_id", "=", product_template_id),
                    ])

                    if not wishlist:
                        in_wishlist = False

                    uom_info = {}

                    if (data.pricelist_item_id.id == 0) or (data.pricelist_item_id.id == False):
                        uom_info["uom_category_id"] = product.uom_category_id.id
                        uom_info["uom_id"] = product.uom_id.id
                        uom_info["uom"] = product.uom_id.name
                        uom_info["uom_description"] = ""
                        uom_info["uom_type"] = product.uom_id.uom_type
                        uom_info["sales_price"] = product.list_price
                        uom_info["discount_price"] = product.discount_price
                        uom_info["discount_percent"] = product.discount_percent
                        uom_info["unit_price"] = 0.0
                        uom_info["currency"] = product.currency_id.name

                    else:
                        uom_info["uom_category_id"] = data.product_uom_category_id.id
                        uom_info["uom_id"] = data.product_uom.id
                        uom_info["uom"] = data.product_uom.name
                        uom_info["uom_description"] = data.pricelist_item_id.uom_description if data.pricelist_item_id.uom_description else ""
                        uom_info["uom_type"] = data.product_uom.uom_type
                        uom_info["sales_price"] = data.pricelist_item_id.fixed_price
                        uom_info["discount_price"] = data.pricelist_item_id.discount_price
                        uom_info["discount_percent"] = data.pricelist_item_id.discount_percent
                        uom_info["unit_price"] = data.pricelist_item_id.unit_price
                        uom_info["currency"] = data.pricelist_item_id.currency_id.name

                    line_subtotal = (data.price_unit * data.product_uom_qty)
                    subtotal += line_subtotal
                    tax_total += (line_subtotal * (data.tax_id.amount / 100))

                    product_list.append({
                        "line_id": data.id,
                        "product_template_id": product_template_id,
                        "product_variant_id": product.id,
                        "name": product.name,
                        "slug": product.slug,
                        "brand": product.brand_id.name if product.brand_id.name else "",
                        "category": product.categ_id.name if product.categ_id.name else "",
                        "image": f"/web/image?model=product.template&id={product_template_id}&field=image_512",
                        "uom_info": uom_info,
                        "product_uom_quantity": data.product_uom_qty,
                        "in_stock": product.in_stock,
                        "in_wishlist": in_wishlist,
                    })

                final_total = subtotal + tax_total

                return {
                    "cart_id": cart.id,
                    "subtotal": subtotal,
                    "tax_total": tax_total,
                    "final_total": final_total,
                    "products": product_list
                }

            else:
                return {"message": "Cart is empty"}
        
        except Exception as e:
            return {"error": e}

    @http.route('/api/cart/add/', auth='public', type='json', csrf=False, cors='*')
    def add_item_to_cart(self, user_id, login_token, product_variant_id, product_uom_category_id, product_uom, product_uom_quantity):
        user = request.env['res.partner'].sudo().search([('id', '=', user_id), ('auth_token', '=', login_token)])
        
        if not user:
            return {'error': 'User not found'}
        
        try:
            website_id = request.env.ref('website.default_website').id
            
            cart = request.env['sale.order'].sudo().search([
                ('partner_id', '=', user_id),
                ("website_id", "=", website_id),
                ('state', '=', 'draft')
            ], limit=1)

            if not cart:
                cart = request.env['sale.order'].sudo().create({
                    'partner_id': user_id,
                    'website_id': website_id,
                    'state': 'draft',
                })

            order_line_item = request.env['sale.order.line'].sudo().search([
                ('order_id', '=', cart.id),
                ('product_id', '=', product_variant_id),
                ('product_uom_category_id', '=', product_uom_category_id),
                ('product_uom', '=', product_uom),
                ('product_uom_qty', '=', product_uom_quantity)
            ])

            if order_line_item:
                return {'message': 'Product already in cart'}
                
            order_line = request.env['sale.order.line'].sudo().create({
                'order_id': cart.id,
                'product_id': product_variant_id,
                'product_uom_category_id': product_uom_category_id,
                'product_uom': product_uom,
                'product_uom_qty': product_uom_quantity
            })

            if not order_line:
                return {'error': 'Something went wrong'}

            data = self.get_cart(user_id, login_token)
            
            return data
        
        except Exception as e:
            return {"error": e}


    @http.route('/api/cart/update/', auth='public', type='json', csrf=False, cors='*')
    def update_item_in_cart(self, user_id, login_token, line_id, product_uom_quantity):
        user = request.env['res.partner'].sudo().search([('id', '=', user_id), ('auth_token', '=', login_token)])
        
        if not user:
            return {'error': 'User not found'}
        
        try:
            website_id = request.env.ref('website.default_website').id
            
            cart = request.env['sale.order'].sudo().search([
                ('partner_id', '=', user_id),
                ("website_id", "=", website_id),
                ('state', '=', 'draft')
            ], limit=1)

            if not cart:
                return {'error': 'Cart not found'}

            order_line_item = request.env['sale.order.line'].sudo().search([
                ('id', '=', line_id)
            ])

            if not order_line_item:
                return {'error': 'Product not in cart'}
                
            line_item = order_line_item.sudo().write({
                'product_uom_qty': product_uom_quantity
            })

            if not line_item:
                return {'error': 'Something went wrong'}

            data = self.get_cart(user_id, login_token)
            
            return data
        
        except Exception as e:
            return {"error": e}
    
    
    @http.route('/api/cart/remove/', auth='public', type='json', csrf=False, cors='*')
    def remove_item_from_cart(self, user_id, login_token, line_id):
        user = request.env['res.partner'].sudo().search([('id', '=', user_id), ('auth_token', '=', login_token)])
        
        if not user:
            return {'error': 'User not found'}
        
        try:
            website_id = request.env.ref('website.default_website').id
            
            cart = request.env['sale.order'].sudo().search([
                ('partner_id', '=', user_id),
                ("website_id", "=", website_id),
                ('state', '=', 'draft')
            ], limit=1)

            if not cart:
                return {'error': 'Cart not found'}

            order_line_item = request.env['sale.order.line'].sudo().search([
                ('id', '=', line_id)
            ])

            if not order_line_item:
                return {'message': 'Product not found'}
                
            order_line_item.sudo().unlink()

            data = self.get_cart(user_id, login_token)
            
            return data
        
        except Exception as e:
            return {"error": e}


    @http.route('/api/cart/add_multiple/', auth='public', type='json', csrf=False, cors='*')
    def add_multiple_items_to_cart(self, user_id, login_token, items):
        user = request.env['res.partner'].sudo().search([('id', '=', user_id), ('auth_token', '=', login_token)])
        
        if not user:
            return {'error': 'User not found'}
        
        try:
            website_id = request.env.ref('website.default_website').id
            
            cart = request.env['sale.order'].sudo().search([
                ('partner_id', '=', user_id),
                ("website_id", "=", website_id),
                ('state', '=', 'draft')
            ], limit=1)

            if not cart:
                cart = request.env['sale.order'].sudo().create({
                    'partner_id': user_id,
                    'website_id': website_id,
                    'state': 'draft',
                })

            for item in items:    
                order_line_item = request.env['sale.order.line'].sudo().search([
                    ('order_id', '=', cart.id),
                    ('product_id', '=', item["product_variant_id"]),
                    ('product_uom_category_id', '=', item["product_uom_category_id"]),
                    ('product_uom', '=', item["product_uom"]),
                    ('product_uom_qty', '=', item["product_uom_quantity"])
                ])

                if order_line_item:
                    if order_line_item.product_uom_qty != item["product_uom_quantity"]:
                        order_line_item.sudo().write([
                            ('product_uom_qty', '=', item["product_uom_quantity"])
                        ])

                else:    
                    order_line = request.env['sale.order.line'].sudo().create({
                        'order_id': cart.id,
                        'product_id': item["product_variant_id"],
                        'product_uom_category_id': item["product_uom_category_id"],
                        'product_uom': item["product_uom"],
                        'product_uom_qty': item["product_uom_quantity"]
                    })

            return {'message': 'Products added in cart'}
        
        except Exception as e:
            return {"error": e}
