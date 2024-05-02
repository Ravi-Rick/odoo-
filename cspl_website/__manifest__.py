{
    'name': "cspl_website",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """Long description of module's purpose""",

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'product', 'stock', 'sale_management', 'website', 'website_sale', 'website_sale_wishlist', 'contacts'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/cspl_website.xml',
        'views/advert.xml',
        'views/mail_template.xml',
        'views/product_category.xml',
        'views/product.xml',
        'views/brand.xml',
        'views/contacts.xml',
        'demo/demo.xml',
        'data/product_tag_data.xml',
    ],
    
    # only loaded in demonstration mode
    'demo': [
    ],
}

