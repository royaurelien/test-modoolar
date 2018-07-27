# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.tools.float_utils import float_round


class AccountMoveLineReconcile(models.TransientModel):
    _inherit = 'account.move.line.reconcile'

    @api.multi
    def trans_rec_get(self):
        print("COIIIIIN COIN COIN !  ")
        context = self._context or {}
        credit = debit = 0
        lines = self.env['account.move.line'].browse(context.get('active_ids', []))
        precision = self.env.user.company_id.currency_id.decimal_places
        for line in lines:
            if not line.full_reconcile_id:
                credit += float_round(line.credit, precision_digits=precision)
                debit += float_round(line.debit, precision_digits=precision)
        writeoff = float_round(debit - credit, precision_digits=precision)
        credit = float_round(credit, precision_digits=precision)
        debit = float_round(debit, precision_digits=precision)
        return {'trans_nbr': len(lines), 'credit': credit, 'debit': debit, 'writeoff': writeoff}
