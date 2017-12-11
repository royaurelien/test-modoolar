# -*- coding:utf-8 -*-
{
    'name': "Domitec Rapports",

    'summary': """ Modification des Rapports """,

    'description': """ Modification des Rapports """,

    'author': "G. Santos",

    'version': '0.1',

    'category': 'Sales',

    # any module necessary for this one to work correctly
    'depends': [
        'sale',  # for sale orders
        'account',  # for invoices (account.invoice)
        'base',  # for ir.actions.report.xml
        'stock',  # for stock.pickings (bls)
    ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'paperformat.xml',
        'reports_layouts.xml',
        'sale_order_reports.xml',

        'invoice/invoice_report.xml',
        'invoice/invoice_action.xml',

        'bl/bl_action.xml',
        'bl/bl_report.xml',

        # marketing rapports
        'views/res_config_settings_view.xml',
    ],

    # 'installable': True,
}
