
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import logging
import pprint
import codecs

logger = logging.getLogger(__name__)

class AccountPaymentOrder(models.Model):
    _inherit = 'account.payment.order'

    @api.multi
    def gen_cfonb_multi(self):

        logger.critical("gen cfonb pour payment orders :  %s " % self.ids)

        file_lines = []

        single_rec = self[0] if len(self) else False

        if not single_rec:
            raise UserError("Aucun enregistrement sélectionné")

        file_lines.append(single_rec._prepare_first_cfonb_line())

        total_amount = 0.0
        eur_currency = self.env.ref('base.EUR')
        transactions_count = 0
        for rec in self:

            first_line = rec._prepare_first_cfonb_line()
            logger.critical("first_line : ")
            logger.critical(first_line)

            cfonb_string = ''
            for line in rec.bank_line_ids:
                if line.currency_id != eur_currency:
                    raise UserError(_(
                        "The currency of payment line '%s' is '%s'. To be "
                        "included in a French LCR, the currency must be EUR.")
                        % (line.name, line.currency_id.name))
                transactions_count += 1
                cfonb_string += rec._prepare_cfonb_line(line, transactions_count)
                total_amount += line.amount_currency
            # cfonb_file = rec.generate_payment_file()
            if cfonb_string:
                file_lines.append(cfonb_string)

            # logger.critical("cfonb line is :")
            # logger.critical(cfonb_string)

        file_lines.append(self._prepare_final_cfonb_line(
            total_amount, transactions_count
        ))
        # pprint.pprint(file_lines)
        # create attachment with the generated file

        file_str = ''.join(file_lines)
        filename = "LCR_export.BNQ"
        attachment = self.env['ir.attachment'].create({
            'res_model': 'account.payment.order',
            # 'res_id': self.ids[0],
            'name': filename,
            'datas': codecs.encode(bytes(file_str, 'ascii'), 'base64'),
            'datas_fname': filename,
        })
        simplified_form_view = self.env.ref(
            'account_payment_order.view_attachment_simplified_form')
        action = {
            # 'name': _('Payment File'),
            'name': 'LCRs',
            'view_mode': 'form',
            'view_id': simplified_form_view.id,
            'res_model': 'ir.attachment',
            'type': 'ir.actions.act_window',
            'target': 'current',
            # 'target': 'new',
            'res_id': attachment.id,
        }
        self.write({
            'date_generated': fields.Date.context_today(self),
            'state': 'generated',
            'generated_user_id': self._uid,
            })
        return action
