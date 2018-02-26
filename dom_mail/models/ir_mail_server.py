# -*- coding:utf-8 -*-

from odoo import models, fields, api

from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo.exceptions import UserError

import logging
logger = logging.getLogger(__name__)


class IrMailServer(models.Model):
    _inherit = "ir.mail_server"

    # en v9, ceci fait que la bounce_address n'est toujours pas set,
    # ce qui fait que le Return-Path du mail sera égal au "From" de l'email,
    # si mail.bounce.alias ou mail.catchall.domain ne sont pas set
    # Si mail.catchall.alias est set, il overridera TOUJOURS le Reply-To.
    # Il faut donc supprimer la clé.
    def _get_default_bounce_address(self):
        return False
