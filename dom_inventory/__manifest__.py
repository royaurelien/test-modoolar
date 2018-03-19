# -*- coding:utf-8 -*-
{
    'name': "Domitec Inventaire ",

    'summary': """ Inventaire """,

    'description': """ Inventaire """,

    'author': "Yziact",

    'version': '0.1',

    'category': 'Stock',

    'depends': [
        'stock',
        'stock_account',
    ],

    'data': [
        'views/stock_inventory.xml',
        'views/stock_quant.xml',
        'views/stock_product.xml',
    ],

    # 'installable': True,
}
