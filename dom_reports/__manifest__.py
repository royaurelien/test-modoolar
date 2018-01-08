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
        'dom_colisage', # BL uses nb_cartons, defined there
    ],

    # always loaded
    'data': [
        # access
        'security/ir.model.access.csv',

        # reports
        'paperformat.xml',
        'reports_layouts.xml',

        # report should be included before action, always
        # (action refers to report, not the other way around)
        'sale_order/sale_order_report.xml',
        'sale_order/sale_order_action.xml',

        'invoice/invoice_report.xml',
        'invoice/invoice_action.xml',

        'bl/bl_report.xml',
        'bl/bl_action.xml',

        # marketing rapports
        'views/res_config_settings_view.xml',

        # vue sale.order.line pour commentaires
        'views/sale_order_line_view.xml',

        # vue et menus dom.comment
        'views/dom_comment_view.xml',

        'views/report_preview_views.xml',
    ],

    # 'installable': True,
}
