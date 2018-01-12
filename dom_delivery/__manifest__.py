# -*- coding:utf-8 -*-
{
    'name': "Domitec Delivery",

    'summary': """ Modification des méthode de livraisons """,

    'description': """ desc""",

    'author': "Yziact",

    'version': '0.1',

    'category': 'Sales',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'delivery',
        'dom_partner',
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',

        'views/delivery_grid.xml',
    ],

    # 'installable': True,
}
