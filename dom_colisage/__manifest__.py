# -*- coding:utf-8 -*-
{
    'name': "Domitec Colisage",

    'summary': """ Gesttion du Colisage pour Domitec """,

    'description': """ Gesttion du Colisage pour Domitec """,

    'author': "G. Santos",

    'version': '0.1',

    'category': 'Sales',

    # any module necessary for this one to work correctly
    'depends': [
        'stock', # for stock.picking
        'sale', # for sale.order
        'delivery', # for view inheriting form sale.order
        'dom_products',
    ],

    # always loaded
    'data': [
        'views/sale_order_view.xml',
        'views/stock_picking_view.xml',
    ],

    # 'installable': True,
}
