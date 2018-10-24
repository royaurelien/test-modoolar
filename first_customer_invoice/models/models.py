# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'
    
    @api.multi
    def _compute_first(self):
        invoices = []
        domain = []
        partners = self.env['account.invoice'].read_group(domain, ['partner_id'], ['partner_id'])
        for partner in partners :
            invoice = self.env['account.invoice'].search([('partner_id', '=', partner['partner_id'][0])], order='date_invoice,create_date', limit = 1)
            invoices.append(invoice)
            invoice.first = True
            
    @api.multi
    def _first_search(self, operator, value):
        recs = self.search([]).filtered(lambda x : x.first is True )
        if recs:
            return [('id', 'in', [x.id for x in recs])]
    
    first = fields.Boolean(string='First', store=False, readonly=True, compute = _compute_first, search='_first_search')

    