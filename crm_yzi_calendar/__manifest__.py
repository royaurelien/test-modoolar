# -*- coding: utf-8 -*-
{
    'name': "CRM Calendar",

    'summary': """ """,

    'description': """ """,

    'author': "Yziact",
    'website': "http://yziact.fr",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'crm_yzi',
        'web',
        # 'web_studio',
    ],

    # always loaded
    'data': [
        # 'views/insert.xml'
        'views/calendar_view.xml',
    ],

    'qweb': [
        # 'static/src/xml/*.xml'
    ],

    # auto_install = fields.Boolean('Automatic Installation',
    # help='An auto-installable module is automatically installed by the '
    # 'system when all its dependencies are satisfied. '
    # 'If the module has no dependency, it is always installed.')

    'auto_install': True,
}

