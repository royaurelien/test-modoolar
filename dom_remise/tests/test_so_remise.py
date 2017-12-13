# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from .test_common import TestCommon
import logging
logger = logging.getLogger(__name__)

class TestSoRemise(TestCommon):

    def setUp(self):
        super(TestSoRemise, self).setUp()

        self.partner = self.env['res.partner'].search([('name', 'ilike', 'test')])
        self.products = [self.product1, self.product2]

        #### Creation des S. O. #####
        # S.O. classique
        self.order_clean = self.create_sale_order(self.partner, self.price_list_100, self.products, 0, False)
        #S.O. avec remise a la ligne
        self.order_discount = self.create_sale_order(self.partner, self.price_list_100, self.products, 10, False)
        #S.O avec remise globale
        self.order_remise = self.create_sale_order(self.partner, self.price_list_100, self.products, 0, self.remise)
        #S.O. cumulant les deux
        self.order_remise_discount = self.create_sale_order(self.partner, self.price_list_100, self.products, 10,self.remise)

        #### Creation des S. O. 100 000 000#####
        # S.O. classique
        self.order_clean_00 = self.create_sale_order(self.partner, self.price_list_100000000, self.products, 0, False)
        # S.O. avec remise a la ligne
        self.order_discount_00 = self.create_sale_order(self.partner, self.price_list_100000000, self.products, 10, False)
        # S.O avec remise globale
        self.order_remise_00 = self.create_sale_order(self.partner, self.price_list_100000000, self.products, 0, self.remise)
        # S.O. cumulant les deux
        self.order_remise_discount_00 = self.create_sale_order(self.partner, self.price_list_100000000, self.products, 10, self.remise)



    def test_so_amount(self):

        # S.O. classique
        self.assertEqual(self.order_clean.amount_ht_net, 200)
        self.assertEqual(self.order_clean.amount_untaxed, 200)
        self.assertEqual(self.order_clean.amount_tax, 40)
        self.assertEqual(self.order_clean.amount_total, 240)

        #S.O. avec remise a la ligne
        self.assertEqual(self.order_discount.amount_ht_net, 180)
        self.assertEqual(self.order_discount.amount_untaxed, 180)
        self.assertEqual(self.order_discount.amount_tax, 36)
        self.assertEqual(self.order_discount.amount_total, 216)

        #S.O avec remise globale
        self.assertEqual(self.order_remise.amount_ht_net, 200)
        self.assertEqual(self.order_remise.amount_untaxed, 180)
        self.assertEqual(self.order_remise.amount_tax, 36)
        self.assertEqual(self.order_remise.amount_total, 216)

        #S.O. cumulant les deux
        self.assertEqual(self.order_remise_discount.amount_ht_net, 180)
        self.assertEqual(self.order_remise_discount.amount_untaxed, 162)
        self.assertEqual(self.order_remise_discount.amount_tax, 32.4)
        self.assertEqual(self.order_remise_discount.amount_total, 194.4)


        #### S.O. 100 000 000 #####
        # S.O. classique
        self.assertEqual(self.order_clean_00.amount_ht_net, 200000000)
        self.assertEqual(self.order_clean_00.amount_untaxed, 200000000)
        self.assertEqual(self.order_clean_00.amount_tax, 40000000)
        self.assertEqual(self.order_clean_00.amount_total, 240000000)

        # S.O. avec remise a la ligne
        self.assertEqual(self.order_discount_00.amount_ht_net, 180000000)
        self.assertEqual(self.order_discount_00.amount_untaxed, 180000000)
        self.assertEqual(self.order_discount_00.amount_tax, 36000000)
        self.assertEqual(self.order_discount_00.amount_total, 216000000)

        # S.O avec remise globale
        self.assertEqual(self.order_remise_00.amount_ht_net, 200000000)
        self.assertEqual(self.order_remise_00.amount_untaxed, 180000000)
        self.assertEqual(self.order_remise_00.amount_tax, 36000000)
        self.assertEqual(self.order_remise_00.amount_total, 216000000)

        # S.O. cumulant les deux
        self.assertEqual(self.order_remise_discount_00.amount_ht_net, 180000000)
        self.assertEqual(self.order_remise_discount_00.amount_untaxed, 162000000)
        self.assertEqual(self.order_remise_discount_00.amount_tax, 32400000)
        self.assertEqual(self.order_remise_discount_00.amount_total, 194400000)

