from odoo import models, fields, api, _, tools
from odoo.exceptions import ValidationError



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

    def _get_default_uom_category(self):
        return self._get_default_uom_id().category_id.id
   
    brand_id = fields.Many2one('cspl_website.brand', tracking=True)
    slug = fields.Char(string='Slug', compute='compute_slug', readonly=True, store=True)
    plain_description = fields.Text(string="Product Description")
    discount_price = fields.Monetary(string="Discount price")
    discount_percent = fields.Float(string="Discount percentage", compute='calculate_discount_percentage', store=True)
    gender = fields.Selection(
        selection=[
            ('Male', 'Male'),
            ('Female', 'Female'),
            ('Unisex', 'Unisex'),
        ],
        string="Gender",
        required=True
    )
    min_age = fields.Integer(required=True, string="Minimum age")
    max_age = fields.Integer(required=True, string="Maximum age")
    in_stock = fields.Boolean(string="In Stock", compute="change_stock_status", store=True)
    aplus_content_id = fields.One2many('aplus_content', 'product_id')
    uom_category_id = fields.Many2one('uom.category', default=_get_default_uom_category, required=True)

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

    @api.onchange("min_age", "max_age")
    def check_age_range(self):
        for instance in self:
            if instance.max_age < instance.min_age:
                raise ValidationError(_("Maximum age cannot be less than minimum age"))
     
    @api.depends("qty_available")
    def change_stock_status(self):
        for product in self:
            if product.product_variant_id.id:
                product.in_stock = product.product_variant_id._is_sold_out()
            else:
                product.in_stock = False


class APlusContent(models.Model):
    _name = "aplus_content"
    _description = "A Plus Content for product"
    _order = "sequence_number"

    product_id = fields.Many2one('product.template')
    sequence_number = fields.Integer(required=True)
    content_type = fields.Selection(
        selection=[
            ('Image', 'Image'),
            ('Video', 'Video'),
             ('Text', 'Text'),
        ],
        string="Content Type",
        required=True
    )
    image = fields.Binary()
    image_description = fields.Text(string="Image Description")
    video_type = fields.Selection(
        selection=[
            ('URL', 'URL'),
            ('Video', 'Video'),
           
        ],
        string="Video Type"
    )
    video_file = fields.Binary()
    video_url = fields.Char()
    heading = fields.Char(string="Heading")
    text_type= fields.Html(string="Text")


class PricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    discount_price = fields.Monetary(string="Discount price")
    discount_percent = fields.Float(
        string="Discount percentage",
        compute='calculate_discount_percentage',
        readonly=True,
        store=True
    )
    unit_price = fields.Monetary(string="Unit price", compute='calculate_unit_price', readonly=True, store=True)
    product_uom_category_id = fields.Many2one(comodel_name='uom.category', related="product_tmpl_id.uom_category_id")
    uom_id = fields.Many2one(comodel_name='uom.uom', domain="[('category_id', '=', product_uom_category_id)]")
    uom_description = fields.Char(string="UOM Description")

    @api.depends("fixed_price", "discount_price")
    def calculate_discount_percentage(self):
        for instance in self:
            if instance.fixed_price == False:
                instance.fixed_price = 0

            if instance.discount_price == False:
                instance.discount_price = 0

            sales_price = instance.fixed_price
            discount_price = instance.discount_price
            
            if sales_price < discount_price:
                raise ValidationError(_("Sales price cannot be less than discount price"))
            
            if (sales_price != 0) and (discount_price != 0):
                discount_amount = sales_price - discount_price
                instance.discount_percent = (discount_amount / sales_price) * 100

            else:
                instance.discount_percent = 0

    @api.depends("fixed_price", "discount_price")
    def calculate_unit_price(self):
        for instance in self:
            if instance.fixed_price:
                if instance.discount_price:
                    instance.unit_price = round((instance.discount_price / instance.uom_id.ratio), 2)
                else:
                    instance.unit_price = round((instance.fixed_price / instance.uom_id.ratio), 2)
