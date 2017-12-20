# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from .test_inv_remise import TestInvRemise
import logging
logger = logging.getLogger(__name__)

class TestAccountRemise(TestInvRemise):

    def setUp(self):
        super(TestAccountRemise, self).setUp()
        move_env = self.env['account.move']
        # self.partner = self.env['res.partner'].search([('name', 'ilike', 'test')])
        self.partner = self.test_user
        self.products = [self.product1, self.product2]

        #### Creation des S. O. #####
        # Move classique
        self.invoice_clean.action_invoice_open()
        self.move_clean =  self.invoice_clean.move_id
        self.credit_clean = self.move_credit_compute(self.move_clean.line_ids)
        self.debit_clean = self.move_debit_compute(self.move_clean.line_ids)
        self.total_untaxed_clean = self.move_total_untaxed(self.move_clean.line_ids)
        self.total_tax_clean = self.move_total_tax(self.move_clean.line_ids)
        self.total_clean = self.move_total(self.move_clean.line_ids)

        #Move avec remise a la ligne
        self.invoice_discount.action_invoice_open()
        self.move_discount = self.invoice_discount.move_id
        self.credit_discount = self.move_credit_compute(self.move_discount.line_ids)
        self.debit_discount = self.move_debit_compute(self.move_discount.line_ids)
        self.total_untaxed_discount = self.move_total_untaxed(self.move_discount.line_ids)
        self.total_tax_discount = self.move_total_tax(self.move_discount.line_ids)
        self.total_discount = self.move_total(self.move_discount.line_ids)

        #S.O avec remise globale
        self.invoice_remise.action_invoice_open()
        self.move_remise = self.invoice_remise.move_id
        self.credit_remise = self.move_credit_compute(self.move_remise.line_ids)
        self.debit_remise = self.move_debit_compute(self.move_remise.line_ids)
        self.total_untaxed_remise = self.move_total_untaxed(self.move_remise.line_ids)
        self.total_tax_remise = self.move_total_tax(self.move_remise.line_ids)
        self.total_remise = self.move_total(self.move_remise.line_ids)

        #Move cumulant les deux
        self.invoice_remise_discount.action_invoice_open()
        self.move_remise_discount = self.invoice_remise_discount.move_id
        self.credit_remise_discount = self.move_credit_compute(self.move_remise_discount.line_ids)
        self.debit_remise_discount = self.move_debit_compute(self.move_remise_discount.line_ids)
        self.total_untaxed_remise_discount = self.move_total_untaxed(self.move_remise_discount.line_ids)
        self.total_tax_remise_discount = self.move_total_tax(self.move_remise_discount.line_ids)
        self.total_remise_discount = self.move_total(self.move_remise_discount.line_ids)

        #### Creation des S. O. 100 000 000#####
        # Move classique
        self.invoice_clean_00.action_invoice_open()
        self.move_clean_00 = self.invoice_clean_00.move_id
        self.credit_clean_00 = self.move_credit_compute(self.move_clean_00.line_ids)
        self.debit_clean_00 = self.move_debit_compute(self.move_clean_00.line_ids)
        self.total_untaxed_clean_00 = self.move_total_untaxed(self.move_clean_00.line_ids)
        self.total_tax_clean_00 = self.move_total_tax(self.move_clean_00.line_ids)
        self.total_clean_00 = self.move_total(self.move_clean_00.line_ids)

        # Move avec remise a la ligne
        self.invoice_discount_00.action_invoice_open()
        self.move_discount_00 = self.invoice_discount_00.move_id
        self.credit_discount_00 = self.move_credit_compute(self.move_discount_00.line_ids)
        self.debit_discount_00 = self.move_debit_compute(self.move_discount_00.line_ids)
        self.total_untaxed_discount_00 = self.move_total_untaxed(self.move_discount_00.line_ids)
        self.total_tax_discount_00 = self.move_total_tax(self.move_discount_00.line_ids)
        self.total_discount_00 = self.move_total(self.move_discount_00.line_ids)

        # S.O avec remise globale
        self.invoice_remise_00.action_invoice_open()
        self.move_remise_00 = self.invoice_remise_00.move_id
        self.credit_remise_00 = self.move_credit_compute(self.move_remise_00.line_ids)
        self.debit_remise_00 = self.move_debit_compute(self.move_remise_00.line_ids)
        self.total_untaxed_remise_00 = self.move_total_untaxed(self.move_remise_00.line_ids)
        self.total_tax_remise_00 = self.move_total_tax(self.move_remise_00.line_ids)
        self.total_remise_00 = self.move_total(self.move_remise_00.line_ids)

        # Move cumulant les deux
        self.invoice_remise_discount_00.action_invoice_open()
        self.move_remise_discount_00 = self.invoice_remise_discount_00.move_id
        self.credit_remise_discount_00 = self.move_credit_compute(self.move_remise_discount_00.line_ids)
        self.debit_remise_discount_00 = self.move_debit_compute(self.move_remise_discount_00.line_ids)
        self.total_untaxed_remise_discount_00 = self.move_total_untaxed(self.move_remise_discount_00.line_ids)
        self.total_tax_remise_discount_00 = self.move_total_tax(self.move_remise_discount_00.line_ids)
        self.total_remise_discount_00 = self.move_total(self.move_remise_discount_00.line_ids)

    def test_so_amount(self):
        """
        la premiere ligne verifie que la piece est equilibree

        les lignes suivantes verifie que chaque montant present en comptabilite
        soit identique a celui sur la facture
        dans l'order suivant, montant hors taxe, montant tax, total TTC

        """


        # Move classique
        self.assertEqual(self.credit_clean, self.debit_clean)
        self.assertEqual(self.total_untaxed_clean, self.invoice_clean.amount_untaxed)
        self.assertEqual(self.total_tax_clean, self.invoice_clean.amount_tax)
        self.assertEqual(self.total_clean, self.invoice_clean.amount_total)

        # Move avec remise a la ligne
        self.assertEqual(self.credit_discount, self.debit_discount)
        self.assertEqual(self.total_untaxed_discount, self.invoice_discount.amount_untaxed)
        self.assertEqual(self.total_tax_discount, self.invoice_discount.amount_tax)
        self.assertEqual(self.total_discount, self.invoice_discount.amount_total)

        # Move avec remise globale
        self.assertEqual(self.credit_remise, self.debit_remise)
        self.assertEqual(self.total_untaxed_remise, self.invoice_remise.amount_untaxed)
        self.assertEqual(self.total_tax_remise, self.invoice_remise.amount_tax)
        self.assertEqual(self.total_remise, self.invoice_remise.amount_total)

        #Move cumulant les deux
        self.assertEqual(self.credit_remise_discount, self.debit_remise_discount)
        self.assertEqual(self.total_untaxed_remise_discount, self.invoice_remise_discount.amount_untaxed)
        self.assertEqual(self.total_tax_remise_discount, self.invoice_remise_discount.amount_tax)
        self.assertEqual(self.total_remise_discount, self.invoice_remise_discount.amount_total)

        #### Move 100 000 000 #####
        # Move classique
        self.assertEqual(self.credit_clean_00, self.debit_clean_00)
        self.assertEqual(self.total_untaxed_clean_00, self.invoice_clean_00.amount_untaxed)
        self.assertEqual(self.total_tax_clean_00, self.invoice_clean_00.amount_tax)
        self.assertEqual(self.total_clean_00, self.invoice_clean_00.amount_total)

        # Move avec remise a la ligne
        self.assertEqual(self.credit_discount_00, self.debit_discount_00)
        self.assertEqual(self.total_untaxed_discount_00, self.invoice_discount_00.amount_untaxed)
        self.assertEqual(self.total_tax_discount_00, self.invoice_discount_00.amount_tax)
        self.assertEqual(self.total_discount_00, self.invoice_discount_00.amount_total)

        # Move avec remise globale
        self.assertEqual(self.credit_remise_00, self.debit_remise_00)
        self.assertEqual(self.total_untaxed_remise_00, self.invoice_remise_00.amount_untaxed)
        self.assertEqual(self.total_tax_remise_00, self.invoice_remise_00.amount_tax)
        self.assertEqual(self.total_remise_00, self.invoice_remise_00.amount_total)

        # Move cumulant les deux
        self.assertEqual(self.credit_remise_discount_00, self.debit_remise_discount_00)
        self.assertEqual(self.total_untaxed_remise_discount_00, self.invoice_remise_discount_00.amount_untaxed)
        self.assertEqual(self.total_tax_remise_discount_00, self.invoice_remise_discount_00.amount_tax)
        self.assertEqual(self.total_remise_discount_00, self.invoice_remise_discount_00.amount_total)
