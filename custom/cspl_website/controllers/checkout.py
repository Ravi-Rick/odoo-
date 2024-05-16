from odoo import http
from odoo.http import request
from odoo import http

class checkout(http.Controller):
    @http.route('/api/proccedtocheckout/', auth='public', type='json', csrf=False, cors='*')
    def procced_to_checkout(self, user_id, login_token):
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
                return {'error': 'Cart is empty'}
            
            if cart.state != 'draft':
                return {'error': f'The order {cart.name} is already confirmed'}

            product_details = []
            
            total_amount = 0
            
            for line in cart.order_line:
                product_details.append({
                    'product_id': line.product_id.id,
                    'product_name': line.product_id.name,
                    'quantity': line.product_uom_qty,
                    'price_unit': line.price_unit,
                    'subtotal': line.price_subtotal,
                })
                
                total_amount += line.price_subtotal
                
            delivery_addresses = []
            for address in user.child_ids.filtered(lambda r: r.type == 'delivery'):
                delivery_addresses.append({
                    'id': address.id,
                    'name': address.name if address.name else '',
                    'street': address.street if address.street else '',
                    'city': address.city if address.city else '',
                    'state': address.state_id.name if address.state_id else '',
                    'country': address.country_id.name if address.country_id else '',
                    'email': address.email if address.email else '',
                    'mobile': address.mobile if address.mobile else '',
                    # 'zip': address.zip if address.zip else ''
                    
                })
                

            
            user_details = {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'phone': user.phone,
                
               
            }

           
            total_amount_with_taxes = total_amount *(1+cart.amount_tax/total_amount)
            
            billing_products = {
                'total_amount': total_amount,
                'total_amount_with_taxes': total_amount_with_taxes,
            }

            return {
                'user_details': user_details,
                'product_details': product_details,
                'billing_products': billing_products,
                'delivery_addresses': delivery_addresses,  
                
            
            }

        except Exception as e:
            return {"error": e}
        
        
    
    @http.route('/api/checkout/', auth='public', type='json', csrf=False, cors='*')
    def checkout(self, user_id, login_token, cart_id=None):  # Accepting cart_id as an optional parameter
        user = request.env['res.partner'].sudo().search([('id', '=', user_id), ('auth_token', '=', login_token)])

        if not user:
            return {'error': 'User not found'}

        try:
            if cart_id:
                cart = request.env['sale.order'].sudo().browse(cart_id)
            else:
                website_id = request.env.ref('website.default_website').id
                cart = request.env['sale.order'].sudo().search([
                    ('partner_id', '=', user_id),
                    ("website_id", "=", website_id),
                    ('state', '=', 'draft')
                ], limit=1)

            if not cart:
                return {'error': 'Cart is empty'}
            
            if cart.state != 'draft':
                return {'error': f'The order {cart.name} is already confirmed'}

            product_details = []
            total_amount = 0

            for line in cart.order_line:
                product_details.append({
                    'product_id': line.product_id.id,
                    'product_name': line.product_id.name,
                    'quantity': line.product_uom_qty,
                    'price_unit': line.price_unit,
                    'subtotal': line.price_subtotal,
                })

                total_amount += line.price_subtotal

            delivery_addresses = []
            for address in user.child_ids.filtered(lambda r: r.type == 'delivery'):
                delivery_addresses.append({
                    'id': address.id,
                    'name': address.name if address.name else '',
                    'street': address.street if address.street else '',
                    'city': address.city if address.city else '',
                    'state': address.state_id.name if address.state_id else '',
                    'country': address.country_id.name if address.country_id else '',
                    'email': address.email if address.email else '',
                    'mobile': address.mobile if address.mobile else '',
                    # 'zip':address.zip if address.zip else ''
                })

            user_details = {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'phone': user.phone,
            }

            total_amount_with_taxes = total_amount * (1 + cart.amount_tax / total_amount)

            billing_products = {
                'total_amount': total_amount,
                'total_amount_with_taxes': total_amount_with_taxes,
            }

            # Change order status to 'sent'
            cart.action_confirm()
            
            # Generate invoice
            # invoice = cart._create_invoices()
            
            # invoice_data = {
            #     'invoice_id': invoice.id,
            #     'invoice_number': invoice.name,
            #     'invoice_date': invoice.invoice_date.strftime('%Y-%m-%d'),
            #     'invoice_amount': invoice.amount_total
            # }
            
            invoice_ids = cart._create_invoices()

            invoice_data = []
            for invoice_id in invoice_ids:
                # if isinstance(invoice_id, int):
                #     invoice = request.env['account.move'].sudo().browse(invoice_id)
             
                    invoice_ulrs=''
                    for invoice in cart.invoice_ids:
                            invoice.write({'state': 'posted'})
                            invoice_ulrs=f"/web/image/{request.env['ir.attachment'].sudo().search([('res_model', '=', 'account.move'), ('res_id', '=', invoice.id)], limit=1).id}"

                    invoice_data = {
                        'invoice_id': invoice.id,
                        'invoice_number': invoice.name,
                        # 'invoice_date': invoice.invoice_date.strftime('%Y-%m-%d'),
                        'invoice_amount': invoice.amount_total,
                        'invoice_ulrs':invoice_ulrs
                    }
                    
                    print('----------------------------------------,',invoice.action_invoice_sent())



            return {
                'user_details': user_details,
                'product_details': product_details,
                'billing_products': billing_products,
                'delivery_addresses': delivery_addresses,
                'cart_id': cart.id,  # Including the cart ID in the response
                'order_status': cart.state, # Including the updated order status in the response
                'invoice_data': invoice_data
            
            }

        except Exception as e:
            return {"error": str(e)}

