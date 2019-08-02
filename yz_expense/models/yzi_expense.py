# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import date


class YziTicket(models.Model):
    _name = 'yzi.ticket'

    #### RELATION ####
    expense = fields.Many2one('yzi.expense')
    product_id = fields.Many2one('product.product', u'Produit', domain=[('is_expensed', '=', True)])
    uom_id = fields.Many2one('product.uom')

    #### DATE ####
    date = fields.Date('Date', default=date.today())

    #### TEXT ####
    desc = fields.Char('Description')
    num_ticket = fields.Char(u"Numéro de Pièce")

    #### NUMERIQUE ####
    unit_ttc = fields.Float(u'Montant unitaire TTC')
    qty = fields.Float(u'Quantité', default=1.0)
    tva_amount = fields.Float(u'Montant TVA')
    ht_amount = fields.Float(u'Montant HT', compute="_get_amount")
    ttc_amount = fields.Float(u'Montant TTC', compute="_get_amount")

    def _get_amount(self):
        for ticket in self :
            ttc = ticket.unit_ttc * ticket.qty
            tva = ticket.tva_amount
            ht = ttc - tva
            ticket.ttc_amount = ttc
            ticket.ht_amount = ht

    ##### ONCHANGE #####
    def _onchange_product_id_values(self, product_id):
        res = {}
        if not product_id:
            return res

        product = self.env['product.product'].browse(product_id)

        #cas generique
        amount_unit = product.standard_price
        res['unit_ttc'] = amount_unit

        # cas des km
        if product.uom_id.id == 9:
            hr_env = self.env['hr.employee']
            hr_obj = hr_env.search([('id','=',self.expense.employee.id)])
            if hr_obj:
                if hr_obj.vehicule_puissance_fiscale.cout:
                    res['unit_ttc'] = hr_obj.vehicule_puissance_fiscale.cout

                else:
                    amount_unit = product.standard_price
                    res['unit_ttc'] = amount_unit
                    raise UserError(_('Problème !'), _('Aucun véhicule n\'a été configuré pour cet employé.'))

            else:
                amount_unit = product.standard_price
                res['unit_ttc'] = amount_unit
                raise UserError(_('Problème !'), _('Aucun utilisateur n\'a été associé avec cet employé.'))

        res['uom_id'] = product.uom_id.id
        return res

    @api.onchange('product_id')
    def _onchange_product_id(self):
        values = self._onchange_product_id_values(self.product_id.id)
        self.update(values)

    @api.onchange('uom_id')
    def _onchange_uom(self):
        values = self._onchange_uom_value(self.uom_id.id, self.product_id.id)
        self.update(values)

    def _onchange_uom_value(self, uom_id, product_id ):
        res = {}
        if not uom_id or not product_id:
            return res
        product = self.env['product.product'].browse(product_id)
        uom = self.env['product.uom'].browse(uom_id)
        if uom.category_id.id != product.uom_id.category_id.id:
            res['warning'] = {'title': _('Warning'), 'message': _('Selected Unit of Measure does not belong to the same category as the product Unit of Measure')}
            res['value'].update({'uom_id': product.uom_id.id})
        return res


class YziExpense(models.Model):
    _name = 'yzi.expense'
    _inherit = ['mail.thread']
    _order = 'date,employee'


    #### RELATION ####
    employee = fields.Many2one('hr.employee', string=u'Employé', required=True)
    validation = fields.Many2one('hr.employee', string=u'Validation par', default=lambda self: self.env['res.users'].browse(self._uid).employee_ids.parent_id.id)
    tickets = fields.One2many('yzi.ticket', 'expense')
    company = fields.Many2one('res.company', default=lambda self: self.env.user.company_id)
    currency_id = fields.Many2one('res.currency', 'Devise', default=lambda self: self.env.user.company_id.currency_id.id)
    fiscal_position = fields.Many2one('account.fiscal.position', string='Position fiscale')
    account_move = fields.Many2one('account.move', string="Mouvement comptable")
    account_move_line = fields.One2many('account.move.line', 'Ecritures comptables', related='account_move.line_ids')

    #### DATE ####
    date = fields.Date('Date', default=date.today(), track_visibility="always")
    date_confirm = fields.Date('Date de Confirmation')
    date_valid = fields.Date('Date de Validation')

    #### TEXT ####
    name = fields.Char('Nom', track_visibility="always")
    desc = fields.Char('Description', required=True)
    note = fields.Text('Notes')

    #### NUMERIQUE ####
    ht_amount = fields.Float(u'Montant HT', compute="_get_amount", track_visibility="always")
    tva_amount = fields.Float(u'Montant TVA', compute="_get_amount", track_visibility="always")
    tva_amount_recup = fields.Float(u'Montant TVA', compute="_get_amount", track_visibility="always")
    ttc_amount = fields.Float(u'Montant TTC', compute="_get_amount", track_visibility="always")
    km_amount = fields.Float(u'Total KMs', compute="_get_amount", track_visibility="always")

    #### SELECTION ####
    state = fields.Selection([
            ('cancel', u'Annulé'),
            ('draft', u'Nouveau'),
            ('waiting', u"En attente d'approbation"),
            ('approved', u'Approuvée'),
            ('paid', u'Payé'),
    ], string=u"Statut", default='draft', track_visibility="always")

    @api.multi
    def confirmation(self):
        for expense in self:
            expense.write({
                'state':'waiting',
                'date_confirm':date.today(),
            })

    @api.multi
    def valid(self):
        for expense in self:
            expense.write({
            'date_valid':date.today(),
            'state':'approved',
        })

    @api.multi
    def cancel(self):
        for expense in self:
            expense.write({
            'state':'cancel',
            'active': False,
        })

    @api.multi
    def draft(self):
        for expense in self:
            expense.write({
            'state':'draft',
            'active': True,
        })

    @api.multi
    def paid(self):

        account_move_env = self.env['account.move']

        for expense in self:
            move_line = expense.get_move__line()
            move_vals = expense.get_move_values(move_line)
            account_move = account_move_env.with_context(dont_create_taxes=True).create(move_vals)

            expense.write({
                'account_move':account_move.id,
                # 'account_move_line': [6,False,move_line_ids],
                'state': 'paid',

            })

    def get_move_values(self, line):
        vals = {}
        journal_env = self.env['account.journal']
        amount = self.ttc_amount
        journal_id = journal_env.search([('name', 'ilike', 'Opérations diverses')]).id
        date = self.date
        narration = u"Frais de déplacement"
        ref = self.employee.name + " : " +self.desc

        vals= {
            'journal_id':journal_id,
            'ref':ref,
            # 'amount':amount,
            'date':date,
            'line_ids':line,
            'narration':narration,
        }

        return vals

    def get_move__line(self, move_id=False):
        journal_env = self.env['account.journal']
        journal_id = journal_env.search([('name', 'ilike', 'Opérations diverses')]).id
        account_move_line_env = self.env['account.move.line']
        account_account_env = self.env['account.account']
        vals=[]
        tva=self.tva_amount_recup
        tva_account = account_account_env.search([('code', '=', '445660')], limit=1)
        total = tva
        account_global_line= self.employee.account.id
        # name = self.employee.account.name

        for ticket in self.tickets:

            product_id = ticket.product_id
            amount = ticket.ht_amount
            if "80%" in ticket.product_id.supplier_taxes_id.name:
                amount = amount + (ticket.tva_amount - (ticket.tva_amount * 0.8))

            total += amount

            account_id = ticket.product_id.property_account_expense_id.id
            amount_residual = 0.0
            debit_chash_basis = debit = amount
            credit_chash_basis = credit = 0.0
            balance = balance_cash_basis = amount
            date = ticket.expense.date
            # move_id = move_id
            quantity = 0.0

            move_line = {
                'name':product_id.display_name,
                'product_id': product_id.id,
                # 'amount' : amount,
                'account_id': account_id,
                'journal_id':journal_id,
                'amount_residual': amount_residual,
                'debit_cash_basis':debit_chash_basis,
                'debit': debit,
                'credit_cash_basis': credit_chash_basis,
                'credit': credit,
                'balance': balance,
                'balance_cash_basis': balance_cash_basis,
                'date': date,
                # 'move_id': move_id,
                'quantity': quantity
            }

            vals.append((0,0,move_line))

        tva_line = {
            'name': tva_account.name,
            # 'amount' : tva,
            'account_id': tva_account.id,
            'journal_id': journal_id,
            'amount_residual': 0.0,
            'debit_cash_basis':tva,
            'debit': tva,
            'credit_cash_basis': 0.0,
            'credit': 0.0,
            'balance': tva,
            'balance_cash_basis': tva,
            'date': self.date,
            # 'move_id': move_id,
            'quantity': 0.0,
        }

        vals.append((0,0,tva_line))

        global_line = {
            'name': "/",
            # 'amount': total,
            'account_id': account_global_line,
            'journal_id': journal_id,
            'amount_residual': -total,
            'debit_cash_basis': 0.0,
            'debit': 0.0,
            'credit_cash_basis': total,
            'credit': total,
            'balance': -total,
            'balance_cash_basis': -total,
            'date': self.date,
            # 'move_id': move_id,
            'quantity': 0.0,
        }

        vals.append((0,0,global_line))

        return vals

    @api.model
    def create(self, vals):
        name = ''
        employee = vals.get('employee', '')
        desc = vals.get('desc', '')


        if employee and desc :
            employee_name = self.env['hr.employee'].browse(employee).name
            name = employee_name + ' ' + desc[:8]

        vals['name']= name
        res = super(YziExpense, self).create(vals)
        return res

    #### ONCHANGE #####
    @api.onchange('employee')
    def onchange_employee(self):
        values = self.onchange_employee_values(self.employee)
        self.update(values)

    def onchange_employee_values(self, employee_id):
        vals = {}
        if employee_id:
            if not employee_id.account_id:
               raise (UserError(u"Attention l'employe n'a pas de compte comptable saisi dans ses parametres employe"))

            fiscal_position = employee_id.fiscal_position or False
            vals['fiscal_position'] = fiscal_position

        return vals
    
    @api.onchange('fiscal_position')
    def onchange_fiscal_position(self):
        # values = self.onchange_fiscal_position_value()
        for ticket in self.tickets :
            ticket.compute_tax()

    #### Compute #####
    @api.multi
    def _get_amount(self):
        for expense in self:
            total_tva = 0.0
            total_tva_recup = 0.0
            total = 0.0
            total_km = 0.0
            for ticket in expense.tickets:
                total_tva += ticket.tva_amount
                total += ticket.ttc_amount

                if ticket.uom_id.id == 9:
                    total_km += ticket.qty

                if "80%" in ticket.product_id.supplier_taxes_id.name:
                    total_tva_recup += ticket.tva_amount * 0.8
                else:
                    total_tva_recup += ticket.tva_amount

            vals = {
                'ht_amount': total - total_tva,
                'tva_amount': total_tva,
                'tva_amount_recup': total_tva_recup,
                'ttc_amount': total,
                'km_amount': total_km,

            }

            expense.update(vals)
