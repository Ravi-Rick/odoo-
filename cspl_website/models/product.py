from odoo import models, fields, api



class Brand(models.Model):
    _name = 'cspl_website.brand'
    _description = 'Product Brands'

    name = fields.Char(string='Brand')
    slug = fields.Char(string='Slug', compute='compute_slug', store=True)
    banner = fields.Binary()
    image = fields.Binary()
    active = fields.Boolean(default=True)
    product_id = fields.One2many(
        comodel_name='product.template', inverse_name='brand_id',
        string='Products of Brand',
        help='Product included in this brand.',
    )

    @api.depends('name')
    def compute_slug(self):
        for brand in self:
            active_languages = self.env['res.lang'].search([('active', '=', True)])
            
            for lang in active_languages:
                slug = brand.with_context(lang=lang.code).name
                data=str(slug).lower()
                data=data.replace('/', '')
                data=data.replace('?', '')
                data=data + f"-{brand.id}"
                brand.with_context(lang=lang.code).slug =  "-".join(data.split(" "))


class ProductCategory(models.Model):
    _inherit = 'product.category'
    
    slug = fields.Char(string='Slug', compute='compute_slug', store=True)
    banner = fields.Binary()
    image = fields.Binary()
    active = fields.Boolean(default=True)

    @api.depends('name')
    def compute_slug(self):
        for category in self:
            active_languages = self.env['res.lang'].search([('active', '=', True)])

            for lang in active_languages:
                slug = category.with_context(lang=lang.code).name
                data=str(slug).lower()
                data=data.replace('/', '')
                data=data.replace('?', '')
                data=data + f"-{category.id}"
                category.with_context(lang=lang.code).slug =  "-".join(data.split(" "))


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    brand_id = fields.Many2one('cspl_website.brand', tracking=True)
    slug = fields.Char(string='Slug', compute='compute_slug', store=True)
    plain_description = fields.Text(string="Product Description")
    discount_price = fields.Monetary(string="Discount price")
    discount_percent = fields.Float(string="Discount percentage", compute='calculate_discount_percentage', store=True)
    in_stock = fields.Boolean(string="In Stock", compute="change_stock_status", store=True)

    @api.depends('name')
    def compute_slug(self):
        for product in self:
            active_languages = self.env['res.lang'].search([('active', '=', True)])

            for lang in active_languages:
                slug = product.with_context(lang=lang.code).name
                data=str(slug).lower()
                data=data.replace('/', '')
                data=data.replace('?', '')
                data=data + f"-{product.id}"
                product.with_context(lang=lang.code).slug =  "-".join(data.split(" "))

    @api.depends("list_price", "discount_price")
    def calculate_discount_percentage(self):
        for product in self:
            if product.list_price == False:
                product.list_price = 0

            if product.discount_price == False:
                product.discount_price = 0

            sales_price = product.list_price
            discount_price = product.discount_price
            
            if (sales_price != 0) and (discount_price != 0):
                discount_amount = sales_price - discount_price
                product.discount_percent = (discount_amount / sales_price) * 100

            else:
                product.discount_percent = 0

    @api.depends("qty_available")
    def change_stock_status(self):
        for product in self:
            if product.product_variant_id.id:
                product.in_stock = product.product_variant_id._is_sold_out()
            else:
                product.in_stock = False
