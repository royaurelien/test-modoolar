# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class mail_message(models.Model):
    _name = 'mail.message'
    _inherit = 'mail.message'

    changed = fields.Boolean('Changed', default=False)
    history_ids = fields.One2many(
        'message.edit.history',
        'message_id',
        'History',
    )

    @api.multi
    def write(self, values):
        """
        Re-write to:
         * Control the user rights
         * Update the history of changes

        To-do:
         * Need to check not only the creator but also the author (or only the author)
        """
        if self._context.get('message_edit'):
            current_partner = self.env.user.partner_id.id
            if current_partner != values.get("author_id") and current_partner != self.sudo().author_id.id:
                raise UserError(
                    _(u'Only the author of the message can edit it.'),
                )
            old_message = {
                'name': self.subject,
                'body': self.body,
                'update_date': fields.Datetime.now(),
            }
            values['history_ids'] = [(0, 0, old_message)]
            values['changed'] = True
        return super(mail_message, self).write(values)

    @api.multi
    def message_format(self):
        """
        Overwrite to pass 'changed'

        Returns:
         * list of dicts per each message in the format for web client
        """
        message_values = super(mail_message, self).message_format()
        for mes_value in message_values:
            message = self.browse(mes_value.get("id"))
            mes_value.update({"changed": message.changed})
        return message_values

    @api.multi
    def get_edit_formview_id(self, access_uid=None):
        """
        The method to get form_view in case of message_edit
        """
        view_id = self.env.ref('message_edit.mail_message_edit_view_form').id
        return view_id
