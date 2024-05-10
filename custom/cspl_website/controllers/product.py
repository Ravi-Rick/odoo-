from odoo import http
from odoo.http import request
from odoo import http



class ProductsAndCategories(http.Controller):
    @http.route('/api/brands/', type='json', methods=['POST'], auth='public', csrf=False, cors='*')
    def get_brands(self):
        brands = request.env["cspl_website.brand"].sudo().search([('active', '=', True)])

        brand_list = []

        for brand in brands:
            brand_list.append({
                "id": brand.id,
                "name": brand.name,
                "slug": brand.slug,
                "banner": f"/web/image?model=cspl_website.brand&id={brand.id}&field=banner",
                "image": f"/web/image?model=cspl_website.brand&id={brand.id}&field=image"
            })

        return brand_list
    
    
    @http.route('/api/categories/', type='json', methods=['POST'], auth='public', csrf=False, cors='*')
    def get_categories(self):
        categories = request.env["product.category"].sudo().search([])

        category_list = []

        for category in categories:
            sub_categories = []

            category_list.append({
                "id": category.id,
                "name": category.name,
                "slug": category.slug,
                "banner": f"/web/image?model=product.category&id={category.id}&field=banner",
                "image": f"/web/image?model=product.category&id={category.id}&field=image",
                "sub_categories": sub_categories
            })

        return category_list
    

    @http.route('/api/product_tags/', type='json', methods=['POST'], auth='public', csrf=False, cors='*')
    def get_product_tags(self):
        tags = request.env["product.tag"].sudo().search([])

        tag_list = []

        for tag in tags:
            tag_list.append({
                "id": tag.id,
                "name": tag.name
            })

        return tag_list
    
    
    @http.route('/api/product_list/', type='json', auth='public', methods=['POST'], csrf=False, cors='*')
    def get_products(self, **kwargs):
        user_id = kwargs.get('user_id', False)
        login_token = kwargs.get('login_token', False)
        brand_id = kwargs.get('brand_id', False)
        category_id = kwargs.get('category_id', False)
        tag_id = kwargs.get('tag_id', False)
        min_price = kwargs.get('min_price', False)
        max_price = kwargs.get('max_price', False)
        gender = kwargs.get('gender', False)
        min_age = kwargs.get('min_age', False)
        max_age = kwargs.get('max_age', False)
        in_stock = kwargs.get('in_stock', False)
        search = kwargs.get('search', False)
        sort_by = kwargs.get('sort_by', '')
        page_no = kwargs.get('page_no', 1)
        page_size = kwargs.get('page_size', 10)
        
        offset = int(page_no - 1) * (page_size)
        limit = int(page_size)
        
        domain = [('is_published', '=', True)]

        if brand_id:
            domain.append(('brand_id.id', '=', brand_id))
        
        if category_id:
            domain.append(('categ_id.id', '=', category_id))
        
        if tag_id:
            domain.append(('product_tag_ids.id', '=', tag_id))

        if (min_price != False) and (max_price != False):
            domain.append(('list_price', '>=', min_price))
            domain.append(('list_price', '<=', max_price))

        if gender:
            domain.append(('gender', '=', gender))

        if (min_age != False) and (max_age != False):
            domain.append(('min_age', '<=', min_age))
            domain.append(('max_age', '>=', max_age))

        if in_stock:
            domain.append(('in_stock', '=', in_stock))

        if search:
            domain.append(('name', 'ilike', search))

        if sort_by != "":
            products = request.env['product.template'].sudo().search(domain, offset=offset, limit=limit, order=sort_by)
        
        else:
            products = request.env['product.template'].sudo().search(domain, offset=offset, limit=limit)
        
        product_list = []

        if user_id and login_token:
            user = request.env['res.partner'].sudo().search([('id', '=', user_id), ('auth_token', '=', login_token)])

            if not user:
                return {'error': 'User not found'}
            
            website_id = request.env.ref('website.default_website').id

            for product in products:
                product_template_id = product.id

                in_wishlist = True
                is_in_cart = False

                wishlist = request.env['product.wishlist'].sudo().search([
                    ("website_id", "=", website_id),
                    ("partner_id", "=", user_id),
                    ("product_id", "=", product_template_id),
                ])

                if not wishlist:
                    in_wishlist = False
                
                cart = request.env['sale.order'].sudo().search([
                    ('partner_id', '=', user_id),
                    ("website_id", "=", website_id),
                    ('state', '=', 'draft')
                ], limit=1)

                if cart and cart.order_line:
                    order_line_item = request.env['sale.order.line'].sudo().search([
                        ('order_id', '=', cart.id),
                        ('product_id', '=', product.product_variant_id.id)
                    ])

                    if order_line_item:
                        is_in_cart = True
        
                uom_list = []
        
                price_list = request.env["product.pricelist.item"].sudo().search(
                    [("product_tmpl_id", "=", product_template_id)],
                    order="fixed_price asc"
                )

                if price_list:
                    for info in price_list:
                        uom_list.append({
                            "pricelist_item_id": info.id,
                            "uom_id": info.uom_id.id,
                            "uom": info.uom_id.name,
                            "uom_description": info.uom_description if info.uom_description else "",
                            "uom_type": info.uom_id.uom_type,
                            "sales_price": info.fixed_price,
                            "discount_price": info.discount_price,
                            "discount_percent": info.discount_percent,
                            "unit_price": info.unit_price,
                            "currency": info.currency_id.name,
                        })

                else:
                    uom_list.append({
                        "pricelist_item_id": 0,
                        "uom_id": 0,
                        "uom": "",
                        "uom_description": "",
                        "uom_type": "",
                        "sales_price": product.list_price,
                        "discount_price": product.discount_price,
                        "discount_percent": product.discount_percent,
                        "unit_price": 0.0,
                        "currency": product.currency_id.name,
                    })
                
                product_list.append({
                    "product_template_id": product_template_id,
                    "product_variant_id": product.product_variant_id.id,
                    "name": product.name,
                    "slug": product.slug,
                    "brand": product.brand_id.name if product.brand_id.name else "",
                    "category": product.categ_id.name if product.categ_id.name else "",
                    "image": f"/web/image?model=product.template&id={product_template_id}&field=image_512",
                    "uom_list": uom_list,
                    "gender": product.gender if product.gender else "",
                    "in_stock": product.in_stock,
                    "in_wishlist": in_wishlist,
                    "in_cart": is_in_cart
                })

        else:
            for product in products:
                product_template_id = product.id

                uom_list = []
        
                price_list = request.env["product.pricelist.item"].sudo().search(
                    [("product_tmpl_id", "=", product_template_id)],
                    order="fixed_price asc"
                )

                if price_list:
                    for info in price_list:
                        uom_list.append({
                            "pricelist_item_id": info.id,
                            "uom_id": info.uom_id.id,
                            "uom": info.uom_id.name,
                            "uom_description": info.uom_description if info.uom_description else "",
                            "uom_type": info.uom_id.uom_type,
                            "sales_price": info.fixed_price,
                            "discount_price": info.discount_price,
                            "discount_percent": info.discount_percent,
                            "unit_price": info.unit_price,
                            "currency": info.currency_id.name,
                        })

                else:
                    uom_list.append({
                        "pricelist_item_id": 0,
                        "uom_id": 0,
                        "uom": "",
                        "uom_description": "",
                        "uom_type": "",
                        "sales_price": product.list_price,
                        "discount_price": product.discount_price,
                        "discount_percent": product.discount_percent,
                        "unit_price": 0.0,
                        "currency": product.currency_id.name,
                    })

                product_list.append({
                    "product_template_id": product_template_id,
                    "product_variant_id": product.product_variant_id.id,
                    "name": product.name,
                    "slug": product.slug,
                    "brand": product.brand_id.name if product.brand_id.name else "",
                    "category": product.categ_id.name if product.categ_id.name else "",
                    "image": f"/web/image?model=product.template&id={product_template_id}&field=image_512",
                    "uom_list": uom_list,
                    "gender": product.gender if product.gender else "",
                    "min_age": product.min_age,
                    "max_age": product.max_age,
                    "in_stock": product.in_stock,
                    "in_wishlist": False,
                    "in_cart": False
                })
            
        total_products = len(products)
        total_pages = total_products // page_size

        category_banner = ""

        if category_id:
            category = request.env["product.category"].sudo().search([("id", "=", category_id)])

            if category and category.banner:
                category_banner = category.banner

        return {
            'current_page': page_no,
            'total_items': total_products,
            'total_pages': total_pages,
            'category_banner': category_banner,
            'products': product_list
        }

    
    @http.route('/api/product/', type='json', auth='public', methods=['POST'], csrf=False, cors='*')
    def get_product_details(self, user_id=False, login_token=False, product_slug=False):
        product = request.env["product.template"].sudo().search([("slug", "=", product_slug)])

        # if len(product) == 0
        if not product:
            return {'error': "Product not found"}

        product_template_id = product.id
        brand_name = product.brand_id.name
        category_id = product.categ_id.id
        category_name = product.categ_id.name
        description = product.plain_description

        if brand_name == False:
            brand_name = ""

        if category_id == False:
            category_id = 0
        
        if category_name == False:
            category_name = ""

        if description == False:
            description = ""

        in_wishlist = False
        is_in_cart = False

        if user_id and login_token:
            user = request.env['res.partner'].sudo().search([('id', '=', user_id), ('auth_token', '=', login_token)])

            if not user:
                return {'error': 'User not found'}

            website_id = request.env.ref('website.default_website').id

            wishlist = request.env['product.wishlist'].sudo().search([
                ("website_id", "=", website_id),
                ("partner_id", "=", user_id),
                ("product_id", "=", product_template_id),
            ])

            if len(wishlist) > 0:
                in_wishlist = True
                
            cart = request.env['sale.order'].sudo().search([
                ('partner_id', '=', user_id),
                ("website_id", "=", website_id),
                ('state', '=', 'draft')
            ], limit=1)

            if cart and cart.order_line:
                order_line_item = request.env['sale.order.line'].sudo().search([
                    ('order_id', '=', cart.id),
                    ('product_id', '=', product.product_variant_id.id)
                ])

                if order_line_item:
                    is_in_cart = True

        image_list = []

        image_list.append(f"/web/image?model=product.template&id={product_template_id}&field=image_512")

        product_images = request.env["product.image"].sudo().search([("product_tmpl_id", "=", product_template_id)])

        if len(product_images) != 0:
            for image in product_images:
                image_list.append(f"/web/image?model=product.image&id={image.id}&field=image_512")

        uom_list = []
        
        price_list = request.env["product.pricelist.item"].sudo().search(
            [("product_tmpl_id", "=", product_template_id)],
            order="fixed_price asc"
        )

        if price_list:
            for info in price_list:
                uom_list.append({
                    "pricelist_item_id": info.id,
                    "uom_id": info.uom_id.id,
                    "uom": info.uom_id.name,
                    "uom_description": info.uom_description if info.uom_description else "",
                    "uom_type": info.uom_id.uom_type,
                    "sales_price": info.fixed_price,
                    "discount_price": info.discount_price,
                    "discount_percent": info.discount_percent,
                    "unit_price": info.unit_price,
                    "currency": info.currency_id.name,
                })

        else:
            uom_list.append({
                "pricelist_item_id": 0,
                "uom_id": 0,
                "uom": "",
                "uom_description": "",
                "uom_type": "",
                "sales_price": product.list_price,
                "discount_price": product.discount_price,
                "discount_percent": product.discount_percent,
                "unit_price": 0.0,
                "currency": product.currency_id.name,
            })

        aplus_content_list = []

        aplus_content = request.env["aplus_content"].sudo().search([
            ("product_id", "=", product_template_id)
        ])

        if aplus_content:
            for content in aplus_content:
                if content.content_type == "Image":
                    aplus_content_list.append({
                        "sequence_number": content.sequence_number,
                        "content_type": content.content_type,
                        "image": f"/web/image?model=aplus_content&id={content.id}&field=image",
                        "image_description": content.image_description if content.image_description else "",
                        "video_type": "",
                        "video_file": "",
                        "video_url": "",
                        "text_type": "",  # New field for Image content
                        "heading": ""     # New field for Image content
                    })

                elif content.content_type == "Video":
                    if content.video_type == "URL":
                        aplus_content_list.append({
                            "sequence_number": content.sequence_number,
                            "content_type": content.content_type,
                            "image": "",
                            "image_description": "",
                            "video_type": content.video_type,
                            "video_file": "",
                            "video_url": content.video_url,
                            "text_type": "",  # New field for Video content
                            "heading": ""     # New field for Video content
                        })

                    elif content.video_type == "Video":
                        aplus_content_list.append({
                            "sequence_number": content.sequence_number,
                            "content_type": content.content_type,
                            "image": "",
                            "image_description": "",
                            "video_type": content.video_type,
                            "video_file": f"/web/image?model=aplus_content&id={content.id}&field=video_file",
                            "video_url": "",
                            "text_type": "",  # New field for Video content
                            "heading": ""     # New field for Video content
                        })
                        
                    elif content.content_type == "Text":
                        aplus_content_list.append({
                            "sequence_number": content.sequence_number,
                            "content_type": content.content_type,
                            "image": "",
                            "image_description": "",
                            "video_type": "",
                            "video_file": "",
                            "video_url": "",
                            "text_type": content.text_type if content.text_type else "",  # New field for Text content
                            "heading": content.heading if content.heading else ""           # New field for Text content
                        })

        return {
            "product_template_id": product_template_id,
            "product_variant_id": product.product_variant_id.id,
            "name": product.name,
            "brand": brand_name,
            "category_id": category_id,
            "category_name": category_name,
            "images": image_list,
            "description": description,
            "uom_list": uom_list,
            "aplus_content": aplus_content_list,
            "gender": product.gender if product.gender else "",
            "min_age": product.min_age,
            "max_age": product.max_age,
            "in_stock": product.in_stock,
            "in_wishlist": in_wishlist,
            "in_cart": is_in_cart,
            "is_variant": product.is_product_variant,
        }
