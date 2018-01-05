# -*- coding:utf-8 -*-
{
    'name': "Domitec Deconditionnement",

    'summary': """ Deconditionnement """,

    'description': """ Deconditionnement """,

    'author': "G. Santos",

    'version': '0.1',

    'category': 'Sales',

    # any module necessary for this one to work correctly
    'depends': [
        'sale',  # for sale orders
    ],

    # always loaded
    'data': [
        'views/sale_order_view.xml',
    ],

    # 'installable': True,
}
