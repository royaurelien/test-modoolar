# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from .test_so_remise import TestSoRemise
import logging
logger = logging.getLogger(__name__)

class TestInvRemise(TestSoRemise):

    def setUp(self):
        super(TestInvRemise, self).setUp()
        invoice_env = self.env['account.invoice']
        self.partner = self.env['res.partner'].search([('name', 'ilike', 'test')])
        self.products = [self.product1, self.product2]

        #### Creation des S. O. #####
        # S.O. classique
        invoice_id  = self.order_clean.action_invoice_create()[0]
        self.invoice_clean = invoice_env.browse(invoice_id)

        #S.O. avec remise a la ligne
        invoice_id =  self.order_discount.action_invoice_create()[0]
        self.invoice_discount = invoice_env.browse(invoice_id)

        #S.O avec remise globale
        invoice_id = self.order_remise.action_invoice_create()[0]
        self.invoice_remise = invoice_env.browse(invoice_id)
        #S.O. cumulant les deux
        invoice_id = self.order_remise_discount.action_invoice_create()[0]
        self.invoice_remise_discount = invoice_env.browse(invoice_id)

        #### Creation des S. O. 100 000 000#####
        # S.O. classique
        invoice_id = self.order_clean_00.action_invoice_create()[0]
        self.invoice_clean_00 = invoice_env.browse(invoice_id)
        # S.O. avec remise a la ligne
        invoice_id = self.order_discount_00.action_invoice_create()[0]
        self.invoice_discount_00 = invoice_env.browse(invoice_id)
        # S.O avec remise globale
        invoice_id = self.order_remise_00.action_invoice_create()[0]
        self.invoice_remise_00 = invoice_env.browse(invoice_id)
        # S.O. cumulant les deux
        invoice_id = self.order_remise_discount_00.action_invoice_create()[0]
        self.invoice_remise_discount_00 = invoice_env.browse(invoice_id)



    def test_so_amount(self):

        # S.O. classique
        self.assertEqual(self.invoice_clean.amount_ht_net, 200)
        self.assertEqual(self.invoice_clean.amount_untaxed, 200)
        self.assertEqual(self.invoice_clean.amount_tax, 40)
        self.assertEqual(self.invoice_clean.amount_total, 240)

        #S.O. avec remise a la ligne
        self.assertEqual(self.invoice_discount.amount_ht_net, 180)
        self.assertEqual(self.invoice_discount.amount_untaxed, 180)
        self.assertEqual(self.invoice_discount.amount_tax, 36)
        self.assertEqual(self.invoice_discount.amount_total, 216)

        #S.O avec remise globale
        self.assertEqual(self.invoice_remise.amount_ht_net, 200)
        self.assertEqual(self.invoice_remise.amount_untaxed, 180)
        self.assertEqual(self.invoice_remise.amount_tax, 36)
        self.assertEqual(self.invoice_remise.amount_total, 216)

        #S.O. cumulant les deux
        self.assertEqual(self.invoice_remise_discount.amount_ht_net, 180)
        self.assertEqual(self.invoice_remise_discount.amount_untaxed, 162)
        self.assertEqual(self.invoice_remise_discount.amount_tax, 32.4)
        self.assertEqual(self.invoice_remise_discount.amount_total, 194.4)


        #### S.O. 100 000 000 #####
        # S.O. classique
        self.assertEqual(self.invoice_clean_00.amount_ht_net, 200000000)
        self.assertEqual(self.invoice_clean_00.amount_untaxed, 200000000)
        self.assertEqual(self.invoice_clean_00.amount_tax, 40000000)
        self.assertEqual(self.invoice_clean_00.amount_total, 240000000)

        # S.O. avec remise a la ligne
        self.assertEqual(self.invoice_discount_00.amount_ht_net, 180000000)
        self.assertEqual(self.invoice_discount_00.amount_untaxed, 180000000)
        self.assertEqual(self.invoice_discount_00.amount_tax, 36000000)
        self.assertEqual(self.invoice_discount_00.amount_total, 216000000)

        # S.O avec remise globale
        self.assertEqual(self.invoice_remise_00.amount_ht_net, 200000000)
        self.assertEqual(self.invoice_remise_00.amount_untaxed, 180000000)
        self.assertEqual(self.invoice_remise_00.amount_tax, 36000000)
        self.assertEqual(self.invoice_remise_00.amount_total, 216000000)

        # S.O. cumulant les deux
        self.assertEqual(self.invoice_remise_discount_00.amount_ht_net, 180000000)
        self.assertEqual(self.invoice_remise_discount_00.amount_untaxed, 162000000)
        self.assertEqual(self.invoice_remise_discount_00.amount_tax, 32400000)
        self.assertEqual(self.invoice_remise_discount_00.amount_total, 194400000)

