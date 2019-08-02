#-*- coding: utf - 8 -*-
{
    'name': "Module Expense by Yziact",

    'summary': """Module Expense custom""",

    'description':
    """
        Module de note de frais spécifique
    """,

    'author': "Yziact",
    'website': "http://www.yziact.fr",

    'category': 'Test',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends':
        [
            'base',
            'hr',
        ],
    # always loaded
    'data': [
        'security/ir.model.access.csv',

        'views/yzi_expense.xml',
        'views/hr_view.xml',
        'views/product_template.xml',
        'reports/report_expense.xml',
        'reports/report_yzi_expense_document.xml',
    ],
}
