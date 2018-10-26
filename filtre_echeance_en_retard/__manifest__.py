# -*- coding: utf-8 -*-
{
    'name': "Filtre échéance en retard",

    'summary': """Filtre échéance en retard""",

    'description': """
           Dans la fiche CONTACT, D'un un filtre "Paiement en retard" pour pouvoir avoir un visuel sur les clients avec une échéance en retard.
    """,

    'author': "Houssem",
    'website': "http://www.itgwana.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Test',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'facturation.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}