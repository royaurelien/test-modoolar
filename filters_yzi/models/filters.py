# -*- coding: utf-8 -*-

from odoo import models, api, fields, _, tools

# import logging
# _logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    partner_id = fields.Many2one('res.partner', delegate=True)


class SaleReport(models.Model):
    _inherit = 'sale.report'

    partner_id = fields.Many2one('res.partner', delegate=True)


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    partner_id = fields.Many2one('res.partner', delegate=True)


class AccountInvoiceReport(models.Model):
    _inherit = 'account.invoice.report'

    price_total_net = fields.Float(string='Total Without Tax Net', readonly=True)
    gr = fields.Many2one(comodel_name='dom.groupe', string=u'Groupe')
    sgr = fields.Many2one(comodel_name='dom.sous.groupe', string=u'Sous-groupe')

    _depends = {
        'account.invoice': [
            'account_id', 'amount_total_company_signed', 'commercial_partner_id', 'company_id',
            'currency_id', 'date_due', 'date_invoice', 'fiscal_position_id',
            'journal_id', 'partner_bank_id', 'partner_id', 'payment_term_id',
            'residual', 'state', 'type', 'user_id',
        ],
        'account.invoice.line': [
            'account_id', 'invoice_id', 'price_subtotal', 'product_id',
            'quantity', 'uom_id', 'account_analytic_id',
        ],
        'product.product': ['product_tmpl_id'],
        'product.template': ['categ_id'],
        'product.uom': ['category_id', 'factor', 'name', 'uom_type'],
        'res.currency.rate': ['currency_id', 'name'],
        'res.partner': ['country_id', 'gr', 'sgr'],
    }


    def _select(self):
        select_str = """
            SELECT sub.id, sub.date, sub.product_id, sub.partner_id,sub.gr, sub.sgr, sub.country_id, sub.account_analytic_id,
                sub.payment_term_id, sub.uom_name, sub.currency_id, sub.journal_id,
                sub.fiscal_position_id, sub.user_id, sub.company_id, sub.nbr, sub.type, sub.state,
                sub.categ_id, sub.date_due, sub.account_id, sub.account_line_id, sub.partner_bank_id,
                sub.product_qty, sub.price_total as price_total,
                sub.price_total_net as price_total_net,
                sub.price_average as price_average,
                COALESCE(cr.rate, 1) as currency_rate, sub.residual as residual, sub.commercial_partner_id as commercial_partner_id
        """
        return select_str


    def _sub_select(self):
        select_str = """
                SELECT ail.id AS id,
                    ai.date_invoice AS date,
                    ail.product_id, ai.partner_id, ai.payment_term_id, ail.account_analytic_id,
                    u2.name AS uom_name,
                    ai.currency_id, ai.journal_id, ai.fiscal_position_id, ai.user_id, ai.company_id,
                    1 AS nbr,
                    ai.type, ai.state, pt.categ_id, ai.date_due, ai.account_id, ail.account_id AS account_line_id,
                    ai.partner_bank_id,
                    SUM ((invoice_type.sign * ail.quantity) / u.factor * u2.factor) AS product_qty,
                    SUM(ail.price_subtotal * invoice_type.sign) AS price_total,
                    SUM(ail.price_subtotal_net * invoice_type.sign) AS price_total_net,
                    SUM(ABS(ail.price_subtotal_signed)) / CASE
                            WHEN SUM(ail.quantity / u.factor * u2.factor) <> 0::numeric
                               THEN SUM(ail.quantity / u.factor * u2.factor)
                               ELSE 1::numeric
                            END AS price_average,
                    ai.residual_company_signed / (SELECT count(*) FROM account_invoice_line l where invoice_id = ai.id) *
                    count(*) * invoice_type.sign AS residual,
                    ai.commercial_partner_id as commercial_partner_id,
                    partner.country_id, partner.gr, partner.sgr
        """
        return select_str

    def _group_by(self):
        group_by_str = """
                     GROUP BY ail.id, ail.product_id, ail.account_analytic_id, ai.date_invoice, ai.id,
                         ai.partner_id, ai.payment_term_id, u2.name, u2.id, ai.currency_id, ai.journal_id,
                         ai.fiscal_position_id, ai.user_id, ai.company_id, ai.type, invoice_type.sign, ai.state, pt.categ_id,
                         ai.date_due, ai.account_id, ail.account_id, ai.partner_bank_id, ai.residual_company_signed,
                         ai.amount_total_company_signed, ai.commercial_partner_id, partner.country_id,partner.gr, partner.sgr
             """
        return group_by_str
