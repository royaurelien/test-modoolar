# -*- coding:utf-8 -*-
{
    'name': "Domitec Remise",

    'summary': """ Modification des Tarifs """,

    'description': """ desc""",

    'author': "Yziact",

    'version': '0.1',

    'category': 'Sales',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'product',
        'sale',
        'account',
        'pivot_view_reports',
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',

        'views/dom_remise.xml',
        'views/res_partner.xml',
        'views/account_invoice.xml',
        'views/sale_order.xml',
        'views/product_template.xml',
    ],

    # 'installable': True,
}
