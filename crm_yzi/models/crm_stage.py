#-*- coding:utf-8 -*-

from odoo import models, fields, api, exceptions, _
from odoo.exceptions import UserError
from datetime import timedelta

class CrmStageInherit(models.Model):
    _name = 'crm.stage'
    _inherit = ['crm.stage', 'mail.thread']

    jalon = fields.Boolean('Jalon')
    hidden_name = fields.Char()


    def unlink(self):

        if self.jalon :
            raise UserError(_("Vous ne pouvez pas supprimer une Etape jalon"))
