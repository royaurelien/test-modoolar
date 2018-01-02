#-*- coding: utf - 8 -*-
{
    'name': "Module Contact by Yziact",

    'summary': """Module Contact custom""",

    'description':
    """
        Module qui modifie les champs de sélection client/fournisseur pour ne pas afficher les contacts.
         L'objectif étant de réduire les risque d'erreur de saisie.
    """,

    'author': "Yziact",
    'website': "http://www.yziact.fr",

    'category': 'Test',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends':
        [
            'base',
            'sale',
            'purchase',
        ],
    # always loaded
    'data':
        [
            'views/invoice.xml',
            'views/sale.xml',
            'views/purchase.xml',

        ],
}
