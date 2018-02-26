# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

"""
Expect script to run tests "quickly" using docker
#!/usr/bin/expect

spawn docker run -ti --rm \
--name odoo_shell \
-e DB_PORT_5432_TCP_ADDR=172.17.0.2 \
-e DB_PORT_5432_TCP_PORT=5432 \
-e DB_ENV_POSTGRES_USER=odoo \
-e DB_ENV_POSTGRES_PASSWORD=odoo123 \
-v odoo_web_data:/var/lib/odoo \
-v /home/gabriel/dev/odoo-yziact:/mnt/extra-addons:z \
odoo_yz_ided openerp-server shell \
-d le_new_db \
-u yz_rmlog \
--log-handler openerp.addons.yz_rmlog.models.rmlog:DEBUG

#--log-handler openerp.addons.odoo-yziact.models.sale_order:DEBUG
#-v /home/gabriel/clients_sauvegarde:/tmp/clients_sauvegarde:z \

#-u odoo-yziact \
#--log-handler :DEBUG

#expect >>>
interact -o -nobuffer -re ">>>.*" return

send "from openerp.modules import module\r"
send "module.run_unit_tests('yz_rmlog', 'this_doesnt_matter')\r"
interact
"""

from openerp.exceptions import UserError, AccessError, MissingError
from datetime import datetime
from dateutil.relativedelta import relativedelta as rd
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT

from test_common import TestCommon
import unittest

import logging
logger = logging.getLogger(__name__)

class TestRmLog(TestCommon):

    def setUp(self):
        super(TestRmLog, self).setUp()

    def test_rmlog_logs(self):
        self.env['ir.config_parameter'].set_param("rmlog.tracked_models", "res.users")

        before_len = len(self.env['rmlog.logrecord'].search([]))

        self.user.unlink()

        # make sure the user record is properly deleted
        with self.assertRaises(MissingError) as w:
            res = self.user.name

        after_len = len(self.env['rmlog.logrecord'].search([]))

        self.assertEqual(before_len, after_len - 1,
            "logrecord was not created for used deletion !")

    def test_rmlog_doesnt_log(self):
        self.env['ir.config_parameter'].set_param("rmlog.tracked_models", "")

        before_len = len(self.env['rmlog.logrecord'].search([]))

        self.user.unlink()

        # make sure the user record is properly deleted
        with self.assertRaises(MissingError) as w:
            res = self.user.name

        after_len = len(self.env['rmlog.logrecord'].search([]))

        self.assertEqual(before_len, after_len,
            "logrecord was created for user deletion when it shouldn't !")

    def test_parse(self):

        # from models.rmlog import parse_tracked_models
        # from models import rmlog
        from ..models.rmlog import parse_tracked_models
        actual = parse_tracked_models("hi  ,  test, he.llo, hi;hi")

        expected = ['hi', 'test', 'he.llo', 'hi;hi']
        self.assertEqual(actual, expected, "parse_tracked_models failed")

        with self.assertRaises(UserError) as w:
            parse_tracked_models([])
