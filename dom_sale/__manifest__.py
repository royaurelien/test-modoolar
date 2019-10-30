# -*- coding:utf-8 -*-
{
    'name': "Modification Sale pour Domitec",

    'summary': """ Modification Sale pour Domitec """,

    'description': """ Custom de view et filtre et autre""",

    'author': "Yziact, Baptiste",

    'version': '0.1',

    'category': 'Sales',

    # any module necessary for this one to work correctly
    'depends': [
        'sale',
        'sale_order_dates',
        'stock'
    ],

    # always loaded
    'data': [
        'views/devis.xml',
        'views/commande.xml',
        'views/sale_report.xml',
    ],

    # 'installable': True,
}
