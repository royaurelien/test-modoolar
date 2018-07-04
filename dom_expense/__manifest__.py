# -*- coding:utf-8 -*-
{
    'name': "Domitec Expense",

    'summary': """ Modification pour la Expense """,

    'description': """ desc""",

    'author': "Yziact",

    'version': '0.1',

    'category': 'Expense',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'account',
        'hr_expense',
        'hr',
    ],

    # always loaded
    'data': [
        'views/hr_employee.xml',
        'views/hr_expense_sheet.xml',
        'views/hr_expense.xml',
    ],

    # 'installable': True,
}
