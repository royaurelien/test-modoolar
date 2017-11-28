# -*- coding:utf-8 -*-
{
    'name': "Domitec Produits",

    'summary': """ Modification des Produits """,

    'description': """ desc""",

    'author': "G. Santos",

    'version': '0.1',

    'category': 'Sales',

    # any module necessary for this one to work correctly
    'depends': [
        'product',
        'stock'
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/product_template.xml',
        'views/product_dang.xml',
        'views/product_family.xml',
    ],

    # 'installable': True,
}
