from odoo import models, fields, api, _


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'



    def set_partner_cron(self):
        partner_env = self.env['res.partner']
        acc_move_lines = self.env['account.move.line'].search([('partner_id', '=', False)])

        for move_line in acc_move_lines:
            if move_line.account_id.reconcile == True :
                if move_line.account_id.user_type_id.name == "Recevable":
                    partner_id = partner_env.search([('property_account_receivable_id', '=', move_line.account_id.id)])
                    if len(partner_id)>1 :
                        for part in partner_id:
                            if part.company_type == 'company':
                                partner_id = part
                    move_line.partner_id = partner_id.id

                elif move_line.account_id.user_type_id.name == "Payable":
                    partner_id = partner_env.search([('property_account_payable_id', '=', move_line.account_id.id)])
                    if len(partner_id)>1 :
                        for part in partner_id:
                            if part.company_type == 'company':
                                partner_id = part

                    move_line.partner_id = partner_id.id
