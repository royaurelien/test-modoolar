# -*- coding:utf-8 -*-

from odoo import models, api, fields

class InvoiceTarif(models.Model):
    _inherit = 'account.invoice'

    #### RELATIONEL #####
    remise = fields.Many2one(comodel_name='dom.remise', string='Remise pied de page (%)')

    #### NUMERIQUE #####
    amount_ht_net = fields.Float('Total HT net', compute='_compute_amount',store=True, track_visibility='onchange')

    @api.onchange('remise')
    def onchange_remise(self):
        vals = self.onchange_remise_values(self.remise)
        self.update(vals)

        self.invoice_line_ids._compute_price()
        self.tax_line_ids._compute_amount_total()

    def onchange_remise_values(self, remise):
        vals = {}
        if remise:
            vals['remise'] = remise

        return vals

    @api.one
    @api.depends('invoice_line_ids.price_subtotal', 'tax_line_ids.amount', 'tax_line_ids.amount_rounding',
                 'currency_id', 'company_id', 'date_invoice', 'type')
    def _compute_amount(self):
        for invoice in self:
            super(InvoiceTarif, invoice)._compute_amount()
            amount_ht_net = 0
            for line in invoice.invoice_line_ids:
                amount_ht_net += line.price_subtotal_net

            invoice.amount_ht_net = amount_ht_net


    @api.multi
    def get_taxes_values(self):
        tax_grouped = {}
        for line in self.invoice_line_ids:
            remise = 0
            if not line.no_remise:
                remise = line.invoice_id.remise.amount

            price_unit = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            price_unit = price_unit - price_unit * (remise / 100)
            # print(price_unit)

            taxes = line.invoice_line_tax_ids.compute_all(price_unit, self.currency_id, line.quantity, line.product_id, self.partner_id)['taxes']
            for tax in taxes:
                val = self._prepare_tax_line_vals(line, tax)
                # print(val)
                key = self.env['account.tax'].browse(tax['id']).get_grouping_key(val)

                if key not in tax_grouped:
                    tax_grouped[key] = val
                else:
                    tax_grouped[key]['amount'] += val['amount']
                    tax_grouped[key]['base'] += val['base']


        return tax_grouped


class InvoiceTarifLine(models.Model):
    _inherit = 'account.invoice.line'

    price_subtotal_net = fields.Monetary(string='Sous-total net', compute='_compute_price', store=True)

    #### BOOLEAN #####
    no_remise = fields.Boolean(string='ne pas appliquer la remise', related='product_id.no_remise')

    @api.one
    @api.depends('price_unit', 'discount', 'invoice_line_tax_ids', 'quantity',
                 'product_id', 'invoice_id.partner_id', 'invoice_id.currency_id', 'invoice_id.company_id',
                 'invoice_id.date_invoice')
    def _compute_price(self):
        super(InvoiceTarifLine, self)._compute_price()
        for line in self :
            currency = line.invoice_id and line.invoice_id.currency_id or None
            vals = {}
            price_subtotal_net = line.price_subtotal
            vals['price_subtotal_net'] = price_subtotal_net

            if not line.no_remise:
                if line.invoice_id.remise:
                    remise = line.invoice_id.remise.amount

                    price_subtotal = line.price_subtotal - line.price_subtotal * (remise / 100)

                    price_total = line.price_total - line.price_total * (remise / 100)

                    vals['price_subtotal'] = price_subtotal
                    vals['price_total'] = price_total

            line.update(vals)


class AccountInvoiceReport(models.Model):
    _inherit = 'account.invoice.report'

    price_total_net = fields.Float(string='Total Without Tax Net', readonly=True)

    def _select(self):
        select_str = """
            SELECT sub.id, sub.date, sub.product_id, sub.partner_id, sub.country_id, sub.account_analytic_id,
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
                    partner.country_id
        """
        return select_str
