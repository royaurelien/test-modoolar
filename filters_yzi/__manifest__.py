# -*- coding: utf-8 -*-
{
    'name': "Filtres avancés",

    'description': """
    Filtres .""",

    'author': "Yziact",
    'website': "http://www.yziact.fr",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'web',
        'sale',
        'account',
        #specifique domitec
        'dom_partner',
    ],

    # always loaded
    'data': [
        #'views/filter_order.xml',
        'views/filter_invoice.xml',
        'views/chiffre_affaires.xml',
    ],
}

