# -*- coding:utf-8 -*-

from odoo import models, api, fields, _
from odoo.exceptions import UserError


class HrExpenseSheet(models.Model):
    _inherit = 'hr.expense.sheet'

    #### RELATIONEL #####
    account_id = fields.Many2one(comodel_name='account.account', string='Compte pour note de frais')


    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        super(HrExpenseSheet, self)._onchange_employee_id()
        vals = self._onchange_employee_values(self.employee_id)
        self.update(vals)


    def _onchange_employee_values(self, employee_id):
        """
        If you need to updtae more values from the onchange_employee_id
        You should inherit this fonction.
        :param employee_id:
        :return: dict of values to update
        """
        values = {}

        if employee_id and employee_id.account_id:
            values['account_id'] = employee_id.account_id.id

        return values


class HrExpense(models.Model):
    _inherit = 'hr.expense'


    """
    Voici la fonction principale appeler par hr.expense.sheet sur ses lignes (lines_ids.action_move_create()) 
    """
    def action_move_create(self):
        '''
        main function that is called when trying to create the accounting entries related to an expense
        '''
        move_group_by_sheet = {}
        for expense in self:
            journal = expense.sheet_id.bank_journal_id if expense.payment_mode == 'company_account' else expense.sheet_id.journal_id
            #create the move that will contain the accounting entries
            acc_date = expense.sheet_id.accounting_date or expense.date
            if not expense.sheet_id.id in move_group_by_sheet:
                move = self.env['account.move'].create({
                    'journal_id': journal.id,
                    'company_id': self.env.user.company_id.id,
                    'date': acc_date,
                    'ref': expense.sheet_id.name,
                    # force the name to the default value, to avoid an eventual 'default_name' in the context
                    # to set it to '' which cause no number to be given to the account.move when posted.
                    'name': '/',
                })
                move_group_by_sheet[expense.sheet_id.id] = move
            else:
                move = move_group_by_sheet[expense.sheet_id.id]
            company_currency = expense.company_id.currency_id
            diff_currency_p = expense.currency_id != company_currency
            #one account.move.line per expense (+taxes..)
            move_lines = expense._move_line_get()

            #create one more move line, a counterline for the total on payable account
            payment_id = False
            total, total_currency, move_lines = expense._compute_expense_totals(company_currency, move_lines, acc_date)
            if expense.payment_mode == 'company_account':

                """
                    la modification de la fonction est ici, on change les test d'existance, du compte sur le journal a celui sur l'expense.
                    et on remplace l'affectation de ce compte de la meme maniere.
                """
                # if not expense.sheet_id.bank_journal_id.default_credit_account_id:
                #     raise UserError(_("No credit account found for the %s journal, please configure one.") % (expense.sheet_id.bank_journal_id.name))
                if not expense.sheet_id.account_id:
                    raise UserError(_(u"Aucun compte n'a été définie pour cette note de frais : %s. Vérifiez la configuration de votre employé et l'onglet 'Autres informations'.") % (expense.sheet_id.id))
                emp_account = expense.sheet_id.account_id.id
                journal = expense.sheet_id.bank_journal_id
                #create payment
                # payment_methods = (total < 0) and journal.outbound_payment_method_ids or journal.inbound_payment_method_ids
                # journal_currency = journal.currency_id or journal.company_id.currency_id
                # payment = self.env['account.payment'].create({
                #     'payment_method_id': payment_methods and payment_methods[0].id or False,
                #     'payment_type': total < 0 and 'outbound' or 'inbound',
                #     'partner_id': expense.employee_id.address_home_id.commercial_partner_id.id,
                #     'partner_type': 'supplier',
                #     'journal_id': journal.id,
                #     'payment_date': expense.date,
                #     'state': 'reconciled',
                #     'currency_id': diff_currency_p and expense.currency_id.id or journal_currency.id,
                #     'amount': diff_currency_p and abs(total_currency) or abs(total),
                #     'name': expense.name,
                # })
                # payment_id = payment.id
            else:
                if not expense.employee_id.address_home_id:
                    raise UserError(_(u"No Home Address found for the employee %s, please configure one.") % (expense.employee_id.name))
                emp_account = expense.employee_id.address_home_id.property_account_payable_id.id

            aml_name = expense.employee_id.name + ': ' + expense.name.split('\n')[0][:64]
            move_lines.append({
                    'type': 'dest',
                    'name': aml_name,
                    'price': total,
                    'account_id': emp_account,
                    'date_maturity': acc_date,
                    'amount_currency': diff_currency_p and total_currency or False,
                    'currency_id': diff_currency_p and expense.currency_id.id or False,
                    'payment_id': payment_id,
                    'expense_id': expense.id,
                    })

            #convert eml into an osv-valid format
            lines = [(0, 0, expense._prepare_move_line(x)) for x in move_lines]
            move.with_context(dont_create_taxes=True).write({'line_ids': lines})
            expense.sheet_id.write({'account_move_id': move.id})
            if expense.payment_mode == 'company_account':
                expense.sheet_id.paid_expense_sheets()
        for move in move_group_by_sheet.values():
            move.post()
        return True

