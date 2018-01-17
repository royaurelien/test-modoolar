# -*- coding: utf-8 -*-
{
    'name': "CRM Custom By Yziact",

    'summary': """""",

    'description': """
    """,

    'author': "Yziact",
    'website': "http://yziact.fr",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'sale',
        'crm',
        'l10n_eu_nace',
        'l10n_fr_naf_ape',
        'l10n_fr_state',
        'module_action',
        # 'crm_voip',
    ],

    # always loaded
    'data': [
        'data/type_rel.xml',
        'security/ir.model.access.csv',

        'views/crm_lead.xml',
        'views/res_partner.xml',
        'views/crm_stage.xml',
    ],
}

