# -*- coding:utf-8 -*-
{
    'name': "Domitec CRM",

    'summary': """ Modification pour la CRM """,

    'description': """ desc""",

    'author': "Yziact",

    'version': '0.1',

    'category': 'Sales',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'crm_yzi',
        'crm',
        'dom_partner',
    ],

    # always loaded
    'data': [
        'views/crm_lead.xml',
        'views/res_partner.xml',
        'views/sale_order.xml',
    ],

    # 'installable': True,
}
