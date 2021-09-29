# -*- coding: utf-8 -*-
{
    'name': "eatman",

    'summary': """
       Here is a change""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly

    'depends': ['base', 'product', 'uom','purchase'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/foodcostview_wizard.xml',
        'views/templates.xml',
        'views/inventory.xml',
        'views/prevision.xml',
        'views/purchase.xml',
        'views/purchase_order.xml',
        'report/eatman_report.xml',
        'views/requirement_wizard.xml',
        'views/preparationslip.xml',
        'demo/allergene.xml'

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
