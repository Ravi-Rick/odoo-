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
        brand_id = kwargs.get('brand_id', False)
        category_id = kwargs.get('category_id', False)
        tag_id = kwargs.get('tag_id', False)
        search = kwargs.get('search', False)
        min_price = kwargs.get('min_price', False)
        max_price = kwargs.get('max_price', False)
        in_stock = kwargs.get('in_stock', False)
        sort_by = kwargs.get('sort_by', '')
        page_no = kwargs.get('page_no', 1)
        page_size = kwargs.get('page_size', 10)
        
        offset = int(page_no - 1) * (page_size)
        limit = int(page_size)
        
        domain = [('is_published', '=', True)]

        if (min_price != False) and (max_price != False):
            domain.append(('list_price', '>=', min_price))
            domain.append(('list_price', '<=', max_price))

        if brand_id:
            domain.append(('brand_id.id', '=', brand_id))
        
        if category_id:
            domain.append(('categ_id.id', '=', category_id))
        
        if tag_id:
            domain.append(('product_tag_ids.id', '=', tag_id))

        if search:
            domain.append(('name', 'ilike', search))

        if in_stock:
            domain.append(('in_stock', '=', in_stock))

        if sort_by != "":
            products = request.env['product.template'].sudo().search(domain, offset=offset, limit=limit, order=sort_by)
        
        else:
            products = request.env['product.template'].sudo().search(domain, offset=offset, limit=limit)

        product_list = []

        if user_id:
            website_id = request.env.ref('website.default_website').id

            for product in products:
                in_wishlist = True

                wishlist = request.env['product.wishlist'].sudo().search([
                    ("website_id", "=", website_id),
                    ("partner_id", "=", user_id),
                    ("product_id", "=", product.id),
                ])

                if not wishlist:
                    in_wishlist = False

                product_list.append({
                    "id": product.id,
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
                })

        else:
            for product in products:
                product_list.append({
                    "id": product.id,
                    "name": product.name,
                    "slug": product.slug,
                    "brand": product.brand_id.name if product.brand_id.name else "",
                    "category": product.categ_id.name if product.categ_id.name else "",
                    "sales_price": product.list_price,
                    "discount_price": product.discount_price,
                    "discount_percent": product.discount_percent,
                    "image": f"/web/image?model=product.template&id={product.id}&field=image_512",
                    "in_stock": product.in_stock,
                    "in_wishlist": False
                })
            
        total_products = len(products)
        total_pages = total_products // page_size
    
        return {
            'current_page': page_no,
            'total_items': total_products,
            'total_pages': total_pages,
            "products": product_list
        }

    
    @http.route('/api/product/', type='json', auth='public', methods=['POST'], csrf=False, cors='*')
    def get_product_details(self, user_id=False, product_slug=False):
        product = request.env["product.template"].sudo().search([("slug", "=", product_slug)])

        # if len(product) == 0
        if not product:
            return {'error': "Product not found"}

        brand_name = product.brand_id.name
        category_name = product.categ_id.name
        description = product.plain_description

        if brand_name == False:
            brand_name = ""

        if category_name == False:
            category_name = ""

        if description == False:
            description = ""

        in_wishlist = False

        if user_id:
            website_id = request.env.ref('website.default_website').id

            wishlist = request.env['product.wishlist'].sudo().search([
                ("website_id", "=", website_id),
                ("partner_id", "=", user_id),
                ("product_id", "=", product.id),
            ])

            if len(wishlist) > 0:
                in_wishlist = True

        image_list = []

        image_list.append(f"/web/image?model=product.template&id={product.id}&field=image_512")

        product_images = request.env["product.image"].sudo().search([("product_tmpl_id", "=", product.id)])

        if len(product_images) != 0:
            for image in product_images:
                image_list.append(f"/web/image?model=product.image&id={image.id}&field=image_512")

        return {
            "id": product.id,
            "name": product.name,
            "brand": brand_name,
            "category": category_name,
            "sales_price": product.list_price,
            "discount_price": product.discount_price,
            "discount_percent": product.discount_percent,
            "images": image_list,
            "description": description,
            "in_stock": product.in_stock,
            "in_wishlist": in_wishlist
        }
