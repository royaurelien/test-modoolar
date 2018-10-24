# -*- coding: utf-8 -*-
{
    'name': "First customer invoice",

    'summary': """
        First customer invoice""",

    'description': """
        First customer invoice
    """,

    'author': "ITGWANA",
    'maintainer': '',

    # lien vers le dépôt git ou site Yziact
    'website': "http://www.itgwana.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Invoice',
    'version': '0.1',
    'license': 'LGPL-3',
    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'account',
    ],
    'external_dependencies': {
        'python': [],
        'bin': [],
    },
    # always loaded
    'data': [
        'views/views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'installable': True,
    'application': False,
    'auto_install': False, 

}
