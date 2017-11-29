# -*- coding:utf-8 -*-
{
    'name': "Domitec Partner",

    'summary': """ Modification des Partners """,

    'description': """ desc""",

    'author': "Yziact",

    'version': '0.1',

    'category': 'Sales',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'account',
    ],

    # always loaded
    'data': [
        'data/dom_famille.xml',
        'security/ir.model.access.csv',

        'views/res_partner.xml',
    ],

    # 'installable': True,
}
