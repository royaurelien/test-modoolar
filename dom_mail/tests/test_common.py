# -*- coding:utf-8 -*-

from openerp.tests.common import TransactionCase

from openerp.exceptions import UserError, AccessError
from datetime import datetime
from dateutil.relativedelta import relativedelta as rd
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT

""" How to run the tests for one module and one module only :

odoo shell :

from openerp.modules import module
module.run_unit_tests('odoo-yziact', 'PROD_DB_1')
"""

class TestCommon(TransactionCase):

    def setUp(self):
        super(TestCommon, self).setUp()

        self.user = self.env['res.users'].create({
            'name': 'Mark User',
            'login': 'user',
            'alias_name': 'mark',
            'email': 'm.u@example.com',
            'signature': '--\nMark',
            'notify_email': 'always',
        })

        '''
        self.so = self.env['sale.order'].create({
        })

        self.inv = self.env['account.invoice'].create({
        })

        sale_order.order_line = [(0, 0, {
            'name': pltdep_prod.name,
            'product_id': pltdep_prod.id,
            'uom_id': 1, # units
            'product_uom_qty': 1,
            'product_uom': pltdep_prod.uom_id.id,
            'price_unit': pltdep_prod.list_price
        })]
        '''
