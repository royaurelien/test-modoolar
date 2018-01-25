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
        'product',
        'sale',
        'account',
        'crm_yzi',
    ],

    # always loaded
    'data': [
        'data/dom_price_list.xml',
        'data/dom_famille.xml',
        'data/dom_presentoir.xml',
        'data/dom_plv.xml',
        'data/type_tier.xml',
        'data/yziact.departement.csv',
        'security/ir.model.access.csv',

        'views/res_partner.xml',
        'views/transporteur.xml',
        'views/famille_client.xml',
        'views/departement.xml',
    ],

    # 'installable': True,
}
