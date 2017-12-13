# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from .test_common import TestCommon
from odoo.exceptions import ValidationError, UserError
import logging
logger = logging.getLogger(__name__)

class TestRemise(TestCommon):

    def setUp(self):
        super(TestRemise, self).setUp()

        self.remise1 = self.create_remise(50)


    def test_remise_creation(self):

        # Remise creation classique
        self.assertEqual(self.remise1.amount, 50)
        self.assertEqual(self.remise1.name, '50.0')

        with self.assertRaises(ValidationError):
            self.remise2 = self.create_remise(-1)

        with self.assertRaises(ValidationError):
            self.remise3 = self.create_remise(1000)

        with self.assertRaises(ValidationError):
            self.remise4 = self.create_remise(50)
