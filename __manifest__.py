# -*- coding: utf-8 -*-
{
    'name': "Weighing Scale with Sales",

    'summary': """
        Hardware Driver for Weighing Scales implementation in Sales""",

    'description': """
        This allows the Weighing Scale Driver to be recognized in the Sales module for non-POS orders.
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['sale','hw_scale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'wizard/sale_weight.xml',
        'views/sale_order_inherit.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}