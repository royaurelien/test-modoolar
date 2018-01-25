# -*- coding:utf-8 -*-
{
    'name': "Domitec lettre de change ",

    'summary': """ Lettre de Change Domitec """,

    'description': """ LCR """,

    'author': "G. Santos",

    'version': '0.1',

    'category': 'Sales',

    'depends': [
        # 'sale',  # for sale orders
        'account',  # for account payment terms
        'dom_reports', # for invoice report
        'account_payment_order', # for account.payment.order model
        'account_banking_fr_lcr', # for additional LCR functions of account.payment.order
    ],

    'data': [
        'views/account_payment_term_view.xml',
        'views/action_server.xml',
        'lcr/lcr.xml',
    ],

    # 'installable': True,
}
