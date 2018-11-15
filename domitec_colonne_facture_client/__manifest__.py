# -*- coding: utf-8 -*-
{
    'name': "colonne_facture_client",

    'summary': """
        colonne_facture_client""",

    'description': """
        Dans FACTURATIONS > Ventes > Factures clients:


        - Rajouter une colonne condition de règlement


        - Supprimer la colonne document d'origine 
    """,

    'author': "ITGwana",
    'maintainer': '',

    # lien vers le dépôt git ou site Yziact
    'website': "http://gitlab.yziact.net/odoo/commons/module",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'account',
    'version': '0.1',
    'license': 'LGPL-3',
    # any module necessary for this one to work correctly
    'depends': [
        'account',
    ],
    'external_dependencies': {
        'python': [],
        'bin': [],
    },
    # always loaded
    'data': [
        'views/account_invoice.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'installable': True,
    'application': False,
    'auto_install': False, 

}
