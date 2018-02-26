# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'


    @api.model
    def create(self, vals):
        parnter_env = self.env['res.partner']

        if vals.get('partner_id'):
            partner = parnter_env.browse(vals.get('partner_id'))

            if not partner.ref:
                partner.get_ref()

            if not partner.property_account_receivable_id:
                partner.action_create_account_customer()

            if not partner.property_account_payable_id:
                partner.action_create_account_supplier()

        return super(AccountInvoice, self).create(vals)


class AccountPaymentTerm(models.Model):
    _inherit = "account.payment.term"


    #### overwrite de la fonction pour nouvelle regle ####
    @api.one
    def compute(self, value, date_ref=False):
        date_ref = date_ref or fields.Date.today()
        amount = value
        result = []
        if self.env.context.get('currency_id'):
            currency = self.env['res.currency'].browse(self.env.context['currency_id'])
        else:
            currency = self.env.user.company_id.currency_id
        for line in self.line_ids:
            if line.value == 'fixed':
                amt = currency.round(line.value_amount)
            elif line.value == 'percent':
                amt = currency.round(value * (line.value_amount / 100.0))
            elif line.value == 'balance':
                amt = currency.round(amount)
            if amt:
                next_date = fields.Date.from_string(date_ref)
                if line.option == 'day_after_invoice_date':
                    next_date += relativedelta(days=line.days)
                elif line.option == 'fix_day_following_month':
                    next_first_date = next_date + relativedelta(day=1, months=1)  # Getting 1st of next month
                    next_date = next_first_date + relativedelta(days=line.days - 1)
                elif line.option == 'end_month_after_fix_day':
                    next_first_date = next_date + relativedelta(days=line.days - 1)
                    next_date = next_first_date + relativedelta(day=31, months=0)  # Getting 1st of next month
                elif line.option == 'last_day_following_month':
                    next_date += relativedelta(day=31, months=1)  # Getting last day of next month
                elif line.option == 'last_day_current_month':
                    next_date += relativedelta(day=31, months=0)  # Getting last day of next month
                result.append((fields.Date.to_string(next_date), amt))
                amount -= amt
        amount = sum(amt for _, amt in result)
        dist = currency.round(value - amount)
        if dist:
            last_date = result and result[-1][0] or fields.Date.today()
            result.append((last_date, dist))
        return result

class AccountPaymentTermLine(models.Model):
    _inherit = "account.payment.term.line"

    option = fields.Selection([
        ('day_after_invoice_date', 'Day(s) after the invoice date'),
        ('fix_day_following_month', 'Day(s) after the end of the invoice month (Net EOM)'),
        ('last_day_following_month', 'Last day of following month'),
        ('last_day_current_month', 'Last day of current month'),
        ('end_month_after_fix_day', 'Fin de mois apres un nombre de jours'),
    ])
