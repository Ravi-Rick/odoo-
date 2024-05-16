import json
from odoo import http,fields
from odoo.http import request
import requests
from odoo import http


class CsplWebsiteFunctions(http.Controller): 
 
    @http.route('/api/langcode',auth='public',type='json',csrf=False,cors='*')
    def LangCode(self,uid=None):
        
        web=request.env['res.lang']
        active_language = web.sudo().search([('active','=',True)])
        language_code =[{"title":lang.name,"code":lang.code} for lang in active_language]
        
        return language_code
    
    
    def categoryListId(self,categories):
        data=[]
        for i in categories:
            data.append(i.id)
            for child in i.child_id:
                data = data+self.categoryListId(child)
        return data
    
    
    def get_pricelist(slef,customer):
        user = request.env['res.partner'].sudo().search([('id','=',customer),('active','=',True)])
        if user:
            if user.company_type == "person":
                return request.env['product.pricelist'].sudo().search([('name','ilike','Public Pricelist')],limit=1).id
            elif user.company_type == "company":
                return request.env['product.pricelist'].sudo().search([('name','ilike','Wholesale Pricelist')],limit=1).id
        else:
            return request.env['product.pricelist'].sudo().search([('name','ilke','Public Pricelist')],limit=1).id
        
        
    def get_price_range(self, product):
        data = []
        for range in product.sudo().product_price_range_ids:
            dict ={}
            dict["id"] = range.id
            dict["minQuantity"] = range.min_qty
            dict["maxQuantity"] = range.max_qty
            dict["price"] = self.tax_included_price_with(prod=product,price=range.price_for_range)
            disc = int(100 - ((dict['price'] / self.tax_included_price_with(prod=product, price=product.list_price)) * 100))
            if  product.compare_list_price:
                disc = int(100 - ((dict['price'] / self.tax_included_price_with(prod=product, price=product.compare_list_price)) * 100))
            dict["discount"] = f"- {disc}%" if disc >0 else ""
            data.append(dict)
        return data
    
    
    def tax_included_price_with(self,prod,price,pricelist=None):
        price_with_taxes = price
        if prod.taxes_id:
            for tax in prod.taxes_id:
                res = tax.sudo().compute_all(price, product=prod, partner=request.env['res.partner'].sudo())
                price_with_taxes = res['total_included']
        return  round(price_with_taxes,2)
    
    
    def tax_included_price_without(self,prod,price,pricelist=None):
        price_with_taxes = price
        if prod.taxes_id:
            for tax in prod.taxes_id:
                res = tax.sudo().compute_all(price, product=prod, partner=request.env['res.partner'].sudo())
                price_with_taxes = res['total_excluded']
        return round(price_with_taxes,2)
    
    
    def get_product_uom(self, prod, pricelist=None, customer_id=None):
        lang = prod._context.get('lang')
        customer_type = "person"
        if customer_id:
            customer_type = request.env['res.partner'].sudo().browse(customer_id).company_type
        uom = [
                {
                    "id": prod.sudo().uom_id.id,
                    "name": prod.sudo().uom_id.name,
                    "value": prod.sudo().uom_id.id,
                    "label": prod.sudo().uom_id.name,
                    "uom_value": prod.sudo().uom_id.factor_inv,
                    "fixed_price": prod.list_price,
                    "price": self.tax_included_price_with(prod=prod,price= prod.list_price,pricelist=pricelist)
                                if customer_type == 'person' 
                                else self.tax_included_price_without(prod=prod,price= prod.list_price,pricelist=pricelist),
                    "currency": prod.currency_id.name,
                    "minQuantity": prod.min_order_qty,
                    "increaseBy":  1,
                    "compare_price": prod.compare_list_price,
                    'discount_percentage': f"- {abs(int(100 - ((self.tax_included_price_with(prod=prod, price=prod.list_price) / prod.compare_list_price) * 100)))}%" if prod.compare_list_price > 0 else '',
                    "priceRange": self.get_price_range(prod)
            }
        ]
        if pricelist:
            if request.env['product.pricelist.item'].sudo().search([('product_tmpl_id', '=', prod.id), ('pricelist_id', '=', pricelist)], limit=1).uom_id:
                uom = []
                for item in request.env['product.pricelist.item'].with_context(lang=lang).sudo().search([('product_tmpl_id', '=', prod.id), ('pricelist_id', '=', pricelist)]):
                    data = []
                    for range in item.sudo().price_range_ids:
                        dict = {}
                        dict["id"] = range.id
                        dict["minQuantity"] = range.min_qty
                        dict["maxQuantity"] = range.max_qty
                        dict["price"] = self.tax_included_price_with(prod=prod,price= range.price_for_range,pricelist=pricelist) if customer_type == 'person' else self.tax_included_price_without(prod=prod,price= range.price_for_range,pricelist=pricelist)
                        dict["discount"] = f"- {abs(int(100 - ((range.price_for_range   / (prod.compare_list_price *item.uom_id.factor_inv)) * 100)))}%" if prod.compare_list_price > 0 else ''
                        data.append(dict)
                    uom.append({
                        "id": item.uom_id.id,
                        "name": item.uom_id.name,
                        "value": item.uom_id.id,
                        "label": item.uom_id.name,
                        "uom_value": item.uom_id.factor_inv,
                        "fixed_price": item.fixed_price,
                        # "price": item.uom_fixed_price,
                        "price": self.tax_included_price_with(prod=prod,price= item.uom_fixed_price,pricelist=pricelist)
                                if customer_type == 'person' 
                                else self.tax_included_price_without(prod=prod,price= item.uom_fixed_price,pricelist=pricelist),
                        "currency": item.currency_id.name,
                        "minQuantity": item.uom_qty,
                        "increaseBy": item.increase_unit_by if item.increase_unit_by > 0 else 1,
                        "compare_price": prod.compare_list_price,
                        'discount_percentage': f"- {abs(int(100 - ((item.uom_fixed_price / (prod.compare_list_price *item.uom_id.factor_inv)) * 100)))}%" if prod.compare_list_price > 0 else '',
                        "priceRange": data
                        })
                    
        return uom
    
    
    
    def get_price(self,prod,pricelist=None):
        price_with_taxes = prod.list_price
        if pricelist:  
            if request.env['product.pricelist.item'].sudo().search(
                    [('product_tmpl_id', '=', prod.id), ('pricelist_id', '=', pricelist)], limit=1).fixed_price:
                price_with_taxes = request.env['product.pricelist.item'].sudo().search(
                    [('product_tmpl_id', '=', prod.id), ('pricelist_id', '=', pricelist)], limit=1).fixed_price
        return price_with_taxes
    
    
    def get_product_ribbon(self, product):
        data = {}
        if product.website_ribbon_id:
            data['name'] = product.website_ribbon_id.html
            data['text_color'] = product.website_ribbon_id.text_color
            data['background_color'] = product.website_ribbon_id.bg_color
        return data
    
    def get_sales_count_str(self,number):
        if 0 == number:
            return f"{int(number)}"
        elif 1 <= number <= 9:
            return f"{int(number)}+"
        elif 10 <= number <= 99:
            return f"{int((number // 10) * 10)}+"
        elif 100 <= number <= 999:
            return f"{int((number // 100) * 100)}+"
        elif 1000 <= number <= 9999:
            return f"{int(number // 1000)}k+"
        elif 10000 <= number <= 99999:
            return f"{int((number // 1000) * 10)}k+"
        
    def get_rating(self,product):
        reviews=[review.rating for review in request.env['user.review'].search([('template_id.id','=',product.id)])]
        return {
                "rating":round(sum(reviews)/len(reviews),1) if len(reviews) > 0 else 0,
                "count":len(reviews)
                }
        
    def get_min_qty(self, product,pricelist=1):
        pricelist_items = request.env['product.pricelist.item'].sudo().search([
                ('product_tmpl_id', '=', product.id),
                ('pricelist_id', '=', pricelist)
            ],limit=1)
        return pricelist_items.min_quantity
    

    @http.route('/api/productInWishlist', auth='public', type='json',csrf=False, cors='*')
    def productInWishlist(self,customer_id=None, product_id=None):
        values = request.env['product.wishlist'].sudo().search([("partner_id","=",customer_id),("product_id","=",request.env['product.template'].sudo().browse(product_id).product_variant_id.id)])
        return True if values else False
    
    
    def get_prod_data(self, products, customer_id = None):
        pricelist = self.get_pricelist(customer_id)
        product_data = []
        for product in products:
            data = {}
            price = self.get_price(product,pricelist)
            uom = self.get_product_uom(prod=product, pricelist=pricelist, customer_id=customer_id)
            data['productId'] = product.id
            data['city'] = product.id
            data['uom'] = uom
            data['uom_id'] = uom[0]['id']
            data['ribbon'] = self.get_product_ribbon(product)
            data['is_customizable'] = product.is_cusomizable
            data['productVariationId'] = product.product_variant_id.id
            data['salesCount'] = self.get_sales_count_str(product.sudo()._compute_sales_count_custome())
            data['attrCombination'] = product.product_variant_id.product_template_variant_value_ids.mapped(
                'product_attribute_value_id.id')
            data['lastmod'] = product.write_date.strftime('%Y-%m-%dT%H:%M:%S')
            data['productName'] = product.name
            data['productSlug'] = product.slug
            data['productImage'] = [
                f'/web/image?model=product.template&id={product.id}&field=image_512',
                f'/web/image?model=product.template&id={product.id}&field=extra_image'
            ] if product.extra_image else [f'/web/image?model=product.template&id={product.id}&field=image_512']
            data['currency'] = product.currency_id.name
            data['base_price'] = product.list_price
            data['price'] = self.tax_included_price_with(prod=product,price=price)
            data['taxes'] = [{'id': tax.id, 'name': tax.name, 'amount': tax.amount, 'price_include': tax.price_include} for
                             tax in product.taxes_id]
            data['compare_price'] = product.compare_list_price
            data['discount_percentage'] = f"- {abs(int(100 - ((self.tax_included_price_with(prod=product, price=price) / product.compare_list_price) * 100)))}%" if product.compare_list_price > 0 else ''
            data['rating'] = self.get_rating(product) if product.allow_review else "hide"
            data['productStock'] = product.sudo().qty_available
            data['minQuantity'] = self.get_min_qty(product=product,pricelist=pricelist) if self.get_min_qty(product=product,pricelist=pricelist) else product.min_order_qty
            data['inWishList'] = self.productInWishlist(customer_id, product.id)
          
            images=[f"/web/image/product.image/{img.id}/image_1024/" for img in request.env['product.image'].search([('product_tmpl_id.id','=',product.id)])]
            images.insert(0,'/web/image?model=product.template&id=' + str(product.id) + '&field=image_1024')
            data["images"]=images if len(images)>0 else ['/web/image?model=product.template&id=' + str(product.id) + '&field=image_1024']
            data['increaseBy'] = max(request.env['product.pricelist.item'].sudo().search(
                [('product_tmpl_id', '=', product.id), ('pricelist_id', '=', 1)], limit=1).increase_unit_by, 1)
            data['category'] = {
                'id': product.categ_id.id,
                'name': product.categ_id.name,
                'display_name': product.categ_id.display_name,
                'slug': product.categ_id.slug
            },
            data['tags'] = [{'id': tag.id, 'tagName': tag.name} for tag in product.product_tag_ids]
            data['priceRange'] = self.get_price_range(product)
            data['saleCount'] = product._compute_sales_count_custome()
            if customer_id and request.env['res.partner'].sudo().browse(customer_id).company_type == 'company':
                data['msrp'] = product.msrp
            if (product.parent_id.id and product.show_child) or product.parent_id.id == False:
                product_data.append(data)
        return {'products': product_data}  



    
        
        