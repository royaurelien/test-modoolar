# -*- coding:utf-8 -*-

from openerp import models, fields, api

from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT
from openerp.exceptions import UserError

import logging
logger = logging.getLogger(__name__)


class MailMail(models.Model):
    _inherit = "mail.mail"

    @api.multi
    def send(self, auto_commit=False, raise_exception=False):

        res = super(MailMail, self).send(auto_commit, raise_exception)
        return res
