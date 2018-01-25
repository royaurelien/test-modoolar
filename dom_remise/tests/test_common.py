# -*- coding:utf-8 -*-

from odoo.tests.common import TransactionCase

""" How to run the tests for one module and one module only :

odoo shell :

from openerp.modules import module
module.run_unit_tests('dom_remise', 'test_one')
"""

class TestCommon(TransactionCase):

    def setUp(self):
        super(TestCommon, self).setUp()
        # some users
        group_manager = self.env.ref('sales_team.group_sale_manager')
        group_user = self.env.ref('sales_team.group_sale_salesman')
        """
        self.manager = self.env['res.users'].create({
            'name': 'Andrew Manager',
            'login': 'manager',
            'alias_name': 'andrew',
            'email': 'a.m@example.com',
            'signature': '--\nAndreww',
            'notify_email': 'always',
            'groups_id': [(6, 0, [group_manager.id])]
        })
        self.user = self.env['res.users'].create({
            'name': 'Mark User',
            'login': 'user',
            'alias_name': 'mark',
            'email': 'm.u@example.com',
            'signature': '--\nMark',
            'notify_email': 'always',
            'groups_id': [(6, 0, [group_user.id])]
        })
        """
        self.test_user = self.env['res.partner'].create({
            'name': 'Test User',
            # 'login': 'test_user',
            # 'password': 'daezr',
            # 'email': 'test@test.com',
            # 'signature': '--\nTest User',
            # 'notify_email': 'never',
            # 'notification_type': 'email',
            # 'groups_id': [(6, 0, [group_user.id])]
        })


        #Creation des list de prix test
        pricelist_env = self.env['product.pricelist']

        self.price_list_100 = pricelist_env.create({
            'name': 'Price list test 100 euros',
            'item_ids':[(0,0,{
                'applied_on':'3_global',
                'compute_price':'fixed',
                'fixed_price':100
            })]
        })
        self.price_list_100000000 = pricelist_env.create({
            'name': 'Price list test 100 000 000 euros',
            'item_ids': [(0, 0, {
                'applied_on': '3_global',
                'compute_price': 'fixed',
                'fixed_price': 100000000
            })]
        })
        # self.remise = self.env['dom.remise'].search([('name','ilike','10.0')])
        # self.product1 = self.env['product.product'].search([('name','ilike', 'Lithofin FVE 5 L')])
        # self.product2 = self.env['product.product'].search([('name','ilike','Lithofin MURO 1L')])
        self.remise = self.env['dom.remise'].create({
            'amount': 10.0,
        })

        self.product1 = self.env['product.product'].create({
            'name': 'test prod one',
            'price': 1.0,
            'invoice_policy': 'order',
            'default_code': '888-888-888',
        })

        self.product2 = self.env['product.product'].create({
            'name': 'test prod two',
            'price': 1.0,
            'invoice_policy': 'order',
            'default_code': '999-999-999',
        })


    def create_remise(self, amount):
        remise_env = self.env['dom.remise']

        remise = remise_env.create({
            'amount':amount
        })

        return remise


    def create_sale_order(self, partner, pricelist, products,discount, remise=False):
        return self.create_sale_order_params(partner, pricelist, products, discount, remise)


    def create_sale_order_params(self, partner, pricelist, products, discount, remise=False):
        sale_env = self.env['sale.order']

        if remise :
            remise= remise.id

        order = sale_env.create({
            'partner_id': partner.id,
            'remise': remise,
            'pricelist_id': pricelist.id,
        })

        for product in products:
            order.order_line = [(0,0, {
                'name': product.name,
                'product_id': product.id,
                'product_uom_qty': 1,
                'product_uom': product.uom_id.id,
                'discount': discount,
            })]

        order.action_confirm()

        return order


    def move_credit_compute(self, lines):
        credit = 0
        for line in lines:
            credit += line.credit

        return credit


    def move_debit_compute(self, lines):
        debit = 0
        for line in lines:
            debit += line.debit

        return debit

    """
    def create_invoice(self, partner, pricelist, products,discount, remise=False):
        return self.create_invoice_params(partner, pricelist, products, discount, remise)

    def create_invoice_params(self, partner, pricelist, products, discount, remise=False):
        invoice_env = self.env['account.invoice']

        if remise :
            remise= remise.id

        invoice = invoice_env.create(
            {
                'partner_id': partner.id,
                'remise':remise,
                'pricelist_id': pricelist.id,
            }
        )
        for product in products:
            invoice.invoice_line_ids  = [(0,0, {
                'name': product.name,
                'product_id': product.id,
                'product_uom_qty': 1,
                'product_uom': product.uom_id.id,
                'discount': discount,
                'account_id': product.property_account_income_id
            })]

        invoice.action_confirm()

        return invoice
    """

    def move_total(self, lines):
        total = 0
        for line in lines:
            if line.name == '/':
                total += line.debit

        return total

    def move_total_tax(self, lines):
        tax = 0
        for line in lines:
            if line.tax_line_id:
                tax += line.credit

        return tax

    def move_total_untaxed(self, lines):
        untaxed = 0
        for line in lines:
            if not line.tax_line_id and line.name != '/' :
                untaxed += line.credit

        return untaxed



