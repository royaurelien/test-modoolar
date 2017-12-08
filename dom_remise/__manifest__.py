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
        'sale',
        'account',
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',

        'views/res_partner.xml',
    ],

    # 'installable': True,
}
