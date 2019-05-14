# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'
    
    @api.multi
    def _compute_first(self):
        partners = self.env['account.invoice'].read_group([], ['partner_id'], ['partner_id'])

        for partner in partners:
            invoice = self.env['account.invoice'].search([('partner_id', '=', partner['partner_id'][0])], order='date_invoice', limit=1)
            invoice.first = True
            
    @api.multi
    def _first_search(self):
        recs = self.search([]).filtered(lambda x : x.first is True )
        if recs:
            return [('id', 'in', [x.id for x in recs])]
    
    first = fields.Boolean(string='First', store=False, readonly=True, compute = _compute_first, search='_first_search')

    