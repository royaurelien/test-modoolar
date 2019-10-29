# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools


class AccountInvoiceReport(models.Model):
    _inherit = 'account.invoice.report'

    _depends = {
        'account.invoice': [
            'account_id', 'amount_total_company_signed', 'commercial_partner_id', 'company_id',
            'currency_id', 'date_due', 'date_invoice', 'fiscal_position_id',
            'journal_id', 'partner_bank_id', 'partner_id', 'payment_term_id',
            'residual', 'state', 'type', 'user_id', 'partner_centrale_id',
        ],
        'account.invoice.line': [
            'account_id', 'invoice_id', 'price_subtotal', 'product_id',
            'quantity', 'uom_id', 'account_analytic_id',
        ],
        'product.product': ['product_tmpl_id'],
        'product.template': ['categ_id'],
        'product.uom': ['category_id', 'factor', 'name', 'uom_type'],
        'res.currency.rate': ['currency_id', 'name'],
        'res.partner': ['country_id'],
    }

    partner_centrale_id = fields.Many2one(comodel_name="res.partner", string="Centrale")

    def _sub_select(self):
        res = super(AccountInvoiceReport, self)._sub_select()

        res += ", ai.partner_centrale_id as partner_centrale_id"

        return res

    def _group_by(self):
        res = super(AccountInvoiceReport, self)._group_by()

        res += ", ai.partner_centrale_id"

        return res

    def _select(self):
        res = super(AccountInvoiceReport, self)._select()

        res += ", sub.partner_centrale_id as partner_centrale_id"

        return res