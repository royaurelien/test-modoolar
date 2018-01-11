#-*- coding:utf-8 -*-

from openerp import models, fields, api, exceptions, _
from openerp.exceptions import UserError
from odoo.osv import expression



class selfartement(models.Model):
    _name = 'yziact.departement'
    _inherit = ['mail.thread']
    _descrition = 'Departement'
    # _order = 'number'

    ##### Numerique ######
    number = fields.Char(u'Numéro')
    name = fields.Char(u'Nom')


    @api.multi
    def name_get(self):
        ### Reprise identique du name_search dans product.product pour ajouter le numero de departement dans le nom
        return [(dep.id, '%s%s' % (dep.number and '%s - ' % dep.number or '', dep.name))
                for dep in self]

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        ### Reprise identique du name_search dans product.product pour ajouter la recherche sur le numero de departement

        if not args:
            args = []

        if name:
            positive_operators = ['=', 'ilike', '=ilike', 'like', '=like']
            deps = self.env['yziact.departement']

            if operator:
                deps = self.search([('number','=',name)]+ args, limit=limit)

            if not deps and operator not in expression.NEGATIVE_TERM_OPERATORS:
                deps = self.search(args + [('number', operator, name)], limit=limit)

            elif not deps and operator in expression.NEGATIVE_TERM_OPERATORS:
                products = self.search(args + ['&', ('number', operator, name), ('name', operator, name)], limit=limit)

        else:
            deps = self.search(args, limit=limit)
        return deps.name_get()
