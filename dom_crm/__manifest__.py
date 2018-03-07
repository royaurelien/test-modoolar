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
        'crm_yzi',
        'crm',
    ],

    # always loaded
    'data': [
        'views/crm_lead.xml',
    ],

    # 'installable': True,
}
