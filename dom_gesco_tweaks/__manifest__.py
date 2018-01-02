# -*- coding:utf-8 -*-
{
    'name': "Domitec Gesco Tweaks",

    'summary': """ Modifications sur la Gesco Spécifique à Domitec """,

    'description': """ Modifications sur la Gesco Spécifique à Domitec """,

    'author': "G. Santos",

    'version': '0.1',

    'category': 'Sales',

    # any module necessary for this one to work correctly
    'depends': [
        'sale',  # for sale orders
    ],

    # always loaded
    'data': [
        'views/sale_order_line_view.xml'
    ],

    # 'installable': True,
}
