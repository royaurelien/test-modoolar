# -*- coding:utf-8 -*-
{
    'name': "Domitec Account",

    'summary': """ Modification Comptable pour Domitec """,

    'description': """ desc""",

    'author': "Yziact",

    'version': '0.1',

    'category': 'Sales',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'sale',
        'account',
        'dom_partner',
    ],

    # always loaded
    'data': [
        'data/partner_seq.xml',
        # 'security/ir.model.access.csv',

        'views/res_partner.xml',
    ],

    # 'installable': True,
}
