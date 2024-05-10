from odoo import http
from odoo.http import request
from odoo import http



class Cart(http.Controller):
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
                
                    product_list.append({
                        "line_id": data.id,
                        "product_template_id": product_template_id,
                        "product_variant_id": product.id,
                        "name": product.name,
                        "slug": product.slug,
                        "brand": product.brand_id.name if product.brand_id.name else "",
                        "category": product.categ_id.name if product.categ_id.name else "",
                        "sales_price": product.list_price,
                        "discount_price": product.discount_price,
                        "discount_percent": product.discount_percent,
                        "image": f"/web/image?model=product.template&id={product.id}&field=image_512",
                        "in_stock": product.in_stock,
                        "in_wishlist": in_wishlist,
                        "product_uom_quantity": data.product_uom_qty
                    })

                return {
                    "cart_id": cart.id,
                    "products": product_list
                }

            else:
                return {"message": "Cart is empty"}
        
        except Exception as e:
            return {"error": e}

    @http.route('/api/cart/add/', auth='public', type='json', csrf=False, cors='*')
    def add_item_to_cart(self, user_id, login_token, product_variant_id, product_uom_quantity):
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
                ('product_uom_qty', '=', product_uom_quantity)
            ])

            if order_line_item:
                return {'message': 'Product already in cart'}
                
            order_line = request.env['sale.order.line'].sudo().create({
                'order_id': cart.id,
                'product_id': product_variant_id,
                'product_uom_qty': product_uom_quantity
            })

            if not order_line:
                return {'error': 'Something went wrong'}

            return {'message': 'Product added in cart'}
        
        except Exception as e:
            return {"error": e}


    @http.route('/api/cart/update/', auth='public', type='json', csrf=False, cors='*')
    def update_item_in_cart(self, user_id, login_token, product_variant_id, product_uom_quantity):
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
                ('order_id', '=', cart.id),
                ('product_id', '=', product_variant_id)
            ])

            if not order_line_item:
                return {'error': 'Product not in cart'}
                
            line_item = order_line_item.sudo().write({'product_uom_qty': product_uom_quantity})

            if not line_item:
                return {'error': 'Something went wrong'}

            return {'message': 'Product updated'}
        
        except Exception as e:
            return {"error": e}
    
    
    @http.route('/api/cart/remove/', auth='public', type='json', csrf=False, cors='*')
    def remove_item_from_cart(self, user_id, login_token, product_variant_id, product_uom_quantity):
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
                ('order_id', '=', cart.id),
                ('product_id', '=', product_variant_id),
                ('product_uom_qty', '=', product_uom_quantity)
            ])

            if not order_line_item:
                return {'message': 'Product not found'}
                
            order_line_item.sudo().unlink()

            return {'message': 'Product removed from the cart'}
        
        except Exception as e:
            return {"error": e}
        
        
        
    
    # @http.route('/api/cart/add/', auth='public', type='json', csrf=False, cors='*')
    # def add_items_to_cart(self, user_id, login_token, product_items):
    #     user = request.env['res.partner'].sudo().search([('id', '=', user_id), ('auth_token', '=', login_token)])
    #     if not user:
    #         return {'error': 'User not found'}

    #     try:
    #         website_id = request.env.ref('website.default_website').id
    #         cart = request.env['sale.order'].sudo().search([
    #             ('partner_id', '=', user_id),
    #             ("website_id", "=", website_id),
    #             ('state', '=', 'draft')
    #         ], limit=1)

    #         if not cart:
    #             cart = request.env['sale.order'].sudo().create({
    #                 'partner_id': user_id,
    #                 'website_id': website_id,
    #                 'state': 'draft',
    #             })

    #         for product_item in product_items:
    #             product_variant_id = product_item['product_variant_id']
    #             product_uom_quantity = product_item['product_uom_quantity']
                

    #             order_line_item = request.env['sale.order.line'].sudo().search([
    #                 ('order_id', '=', cart.id),
    #                 ('product_id', '=', product_variant_id),
    #                 ('product_uom_qty', '=', product_uom_quantity)
    #             ])

    #             if order_line_item:
    #                 continue  

    #             order_line = request.env['sale.order.line'].sudo().create({
    #                 'order_id': cart.id,
    #                 'product_id': product_variant_id,
    #                 'product_uom_qty': product_uom_quantity
    #             })

    #             if not order_line:
    #                 return {'error': 'Something went wrong'}

    #         return {'message': 'Products added to cart'}

    #     except Exception as e:
    #         return {"error": str(e)}
    
    
    
    # @http.route('/api/cart/add/', auth='public', type='json', csrf=False, cors='*')
    # def add_items_to_cart(self, user_id, login_token, product_items):
    #     user = request.env['res.partner'].sudo().search([('id', '=', user_id), ('auth_token', '=', login_token)])
    #     if not user:
    #         return {'error': 'User not found'}

    #     try:
    #         website_id = request.env.ref('website.default_website').id
    #         cart = request.env['sale.order'].sudo().search([
    #             ('partner_id', '=', user_id),
    #             ("website_id", "=", website_id),
    #             ('state', '=', 'draft')
    #         ], limit=1)

    #         if not cart:
    #             cart = request.env['sale.order'].sudo().create({
    #                 'partner_id': user_id,
    #                 'website_id': website_id,
    #                 'state': 'draft',
    #             })

    #         for product_item in product_items:
    #             product_variant_id = product_item['product_variant_id']
    #             product_uom_quantity = product_item['product_uom_quantity']
    #             product_uom_name = product_item.get('product_uom_name')  # Get the value or None if key doesn't exist

    #             order_line_item = request.env['sale.order.line'].sudo().search([
    #                 ('order_id', '=', cart.id),
    #                 ('product_id', '=', product_variant_id),
    #                 ('product_uom_qty', '=', product_uom_quantity)
    #             ])

    #             if order_line_item:
    #                 continue  # Skip if the product is already in the cart

    #             if product_uom_name:
    #                 uom_id = request.env['product.uom'].sudo().search([('name', '=', product_uom_name)], limit=1).id
    #             else:
    #                 # Use a default UoM or skip the product item
    #                 uom_id = 1  # Replace 1 with the ID of your desired default UoM

    #             order_line = request.env['sale.order.line'].sudo().create({
    #                 'order_id': cart.id,
    #                 'product_id': product_variant_id,
    #                 'product_uom_qty': product_uom_quantity,
    #                 'product_uom': uom_id
    #             })

    #             if not order_line:
    #                 return {'error': 'Something went wrong'}

    #         return {'message': 'Products added to cart'}

    #     except Exception as e:
    #         return {"error": str(e)}

