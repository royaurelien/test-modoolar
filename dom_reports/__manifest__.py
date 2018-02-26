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
        'purchase',  # for purchase.order (com_fourn)
        'dom_remise', # Devis/BC/Facture uses this
        'dom_colisage', # BL uses nb_cartons, defined there
        'dom_delivery', # BL uses nb_cartons, defined there
        'dom_decond', # BL uses nb_cartons, defined there
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
        # devis/bc
        'sale_order/sale_order_report.xml',
        'sale_order/sale_order_action.xml',

        # facture
        'invoice/invoice_report.xml',
        'invoice/invoice_action.xml',

        # facture
        'facture_noheader/fac_nohdr_action.xml',
        'facture_noheader/fac_nohdr_report.xml',

        # BL
        'bl/bl_report.xml',
        'bl/bl_action.xml',

        # commande fournisseur
        'purchase/com_fourn_report.xml',
        'purchase/com_fourn_action.xml',

        # marketing rapports
        'views/res_config_settings_view.xml',

        # vue sale.order.line pour commentaires
        # 'views/sale_order_line_view.xml',

        # vue et menus dom.comment
        # 'views/dom_comment_view.xml',

        # new comments
        'views/product_template.xml',

        # aperçus des rapports
        'views/report_preview_views.xml',

        'views/res_company_view.xml',

        # datas
        'data/marketing_data.xml',

        # widget injection
        'injection.xml',
    ],

    'qweb': [
        'static/src/xml/*.xml'
    ],

    # 'installable': True,
}
