
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

        user_group_stock_user = self.env.ref('stock.group_stock_user')
        user_group_stock_manager = self.env.ref('stock.group_stock_manager')

        Users = self.env['res.users']

        self.user_stock_manager = Users.create({
            'name': 'Julie Tablier',
            'login': 'julie',
            'email': 'j.j@example.com',
            'notification_type': 'inbox',
            'groups_id': [(6, 0, [user_group_stock_manager.id])],
        })

        self.test_user = Users.create({
            'name': 'Test User',
            'login': 'test_user',
            'password': 'daezr',
            # 'email': 'test@test.com',
            'signature': '--\nTest User',
            # 'notify_email': 'never',
            # 'notification_type': 'email',
            'groups_id': [(6, 0, [group_user.id])]
        })

        # Warehouses
        self.warehouse_1 = self.env['stock.warehouse'].create({
            'name': 'Base Warehouse',
            'reception_steps': 'one_step',
            'delivery_steps': 'ship_only',
            'code': 'BWH'})

        # Locations
        self.location_1 = self.env['stock.location'].create({
            'name': 'TestLocation1',
            'posx': 3,
            'location_id': self.warehouse_1.lot_stock_id.id,
        })

        # Products
        Product = self.env['product.product']
        self.product1 = Product.create({
            'name': 'test prod one',
            'price': 1.0,
            'invoice_policy': 'order',
            'default_code': '888-888-888',
            'nb_par_colis': 10,
        })

        self.product2 = Product.create({
            'name': 'test prod two',
            'price': 1.0,
            'invoice_policy': 'order',
            'default_code': '999-999-999',
            'nb_par_colis': 2,
        })

        self.product3 = Product.create({
            'name': 'test prod three',
            'price': 1.0,
            'invoice_policy': 'order',
            'default_code': '777-777-777',
            'nb_par_colis': 0,
        })

        self.prod_par10 = Product.create({
            'name': 'test prod 1',
            'price': 1.0,
            'invoice_policy': 'order',
            # 'default_code': 'a',
            'nb_par_colis': 10,
        })

        self.prod_par5 = Product.create({
            'name': 'test prod 2',
            'price': 1.0,
            'invoice_policy': 'order',
            # 'default_code': 'a',
            'nb_par_colis': 5,
        })

        self.prod_par2 = Product.create({
            'name': 'test prod 3',
            'price': 1.0,
            'invoice_policy': 'order',
            'default_code': 'a',
            'nb_par_colis': 2,
        })

        self.prod_par1 = Product.create({
            'name': 'test prod 4',
            'price': 1.0,
            'invoice_policy': 'order',
            'default_code': 'a',
            'nb_par_colis': 1,
        })

    def _create_move(self, picking, product, qty, **values):
        # TDE FIXME: user as parameter
        Move = self.env['stock.move'].sudo(self.user_stock_manager)
        # simulate create + onchange
        move = Move.new({
            'product_id': product.id,
            'product_uom_qty': qty,
            'quantity_done': qty,
            'location_id': picking.location_id.id,
            'location_dest_id': picking.location_dest_id.id,
            'picking_id': picking.id,
        })
        move.onchange_product_id()
        move_values = move._convert_to_write(move._cache)
        move_values.update(**values)
        return Move.create(move_values)

    def _create_picking(self, ptype, warehouse):
        """
        ptype is "in" or "out"
        """
        suppliers_loc_id = self.env.ref('stock.stock_location_suppliers').id
        customers_loc_id = self.env.ref('stock.stock_location_suppliers').id

        Picking = self.env['stock.picking']

        picking_values = {}
        if ptype == "in":
            picking_values = {
                'picking_type_id': warehouse.in_type_id.id,
                'location_id': suppliers_loc_id,
                'location_dest_id': warehouse.lot_stock_id.id,
            }
        elif ptype == "out":
            picking_values = {
                'picking_type_id': warehouse.out_type_id.id,
                'location_id': warehouse.lot_stock_id.id,
                'location_dest_id': customers_loc_id,
            }
        return Picking.create(picking_values)


    def test_colisage_picking_nb_cartons(self):

        def make_asserts(qt1, qt2, qt3, expected):
            pick = self._create_picking("out", self.warehouse_1)
            self._create_move(pick, self.product1, qt1)
            self._create_move(pick, self.product2, qt2)
            self._create_move(pick, self.product3, qt3)
            # creating a move with a picking_id of our picking
            # doesn't trigger the compute (?)
            pick._compute_nb_cartons()
            self.assertEqual(pick.nb_cartons, expected)

        def make_asserts_tupled(expected, tuple_list):
            """
            tuple list is a list of (product, qty), that will be added as move lines to the picking
            """
            pick = self._create_picking("out", self.warehouse_1)
            for tup in tuple_list:
                self._create_move(pick, tup[0], tup[1])
            # creating a move with a picking_id of our picking
            # doesn't trigger the compute (?)
            pick._compute_nb_cartons()
            self.assertEqual(pick.nb_cartons, expected)

        make_asserts(0, 0, 0, 0)

        make_asserts(10, 3, 0, 3)
        make_asserts(1, 3, 0, 3)
        make_asserts(1, 1, 4, 6)

        make_asserts_tupled(18, [
            (self.prod_par10, 10),
            (self.prod_par10, 50),
            (self.prod_par5, 50),
            (self.prod_par2, 2),
            (self.prod_par1, 1)
        ])

        make_asserts_tupled(4, [
            (self.prod_par2, 2),
            (self.prod_par1, 3)
        ])
