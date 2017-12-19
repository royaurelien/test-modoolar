from itertools import groupby

# self contains the env from the odoo shell
def fix_products(self):

    prods = self.env['product.product'].search([])
    res_dict = {}

    for k, g in groupby(prods, lambda x: x.product_tmpl_id.id):
        if k in res_dict:
            res_dict[k].extend([x for x in g])
        else:
            res_dict.update({k: [x for x in g]})

    for key in res_dict:
        prod_group = res_dict[key]

        bc_prod = ref_prod = None

        if len(prod_group) != 2:
            continue

        try :
            bc_prod = list(filter(lambda x: x.barcode, prod_group))[0]
            ref_prod = list(filter(lambda x: x.default_code, prod_group))[0]
        except IndexError as e:
            print("barcode or ref not found in either product")

        if not bc_prod or not ref_prod:
            continue

        line1 = self.env['sale.order.line'].search([('product_id','=',bc_prod.id)])
        line2 = self.env['sale.order.line'].search([('product_id','=',ref_prod.id)])

        # have to store, delete, and then affect...
        # because barcode is unique, and default_code too
        if not line1:
            barcode = bc_prod.barcode
            bc_prod.unlink()
            ref_prod.barcode = barcode
        elif not line2:
            default_code = ref_prod.default_code
            ref_prod.unlink()
            bc_prod.default_code = default_code
        else:
            print("both products are linked to lines... can't unlink")


def fix_qtys(self):

    unit = self.env['product.uom'].search([('name', 'ilike', 'unit')], limit=1)

    prods = self.env['product.product'].search([])

    for p in prods:

        # if product is tied in move, put move in draft and remove it:
        moves = self.env['stock.move'].search([('product_id', '=', p.id)])
        for move in moves:
            move.state = 'draft'
            move.unlink()

        p.write({
            'uom_id': unit.id,
            'uom_po_id': unit.id
        })

"""

inv_lines = self.env['stock.inventory.line'].search([])
for line in inv_lines: line.unlink()

moves = self.env['stock.move'].search([])
for m in moves: m.state = 'draft'; m.unlink()

import os, sys
os.chdir('/mnt/extra-addons')
sys.path.append(os.getcwd())
from fix_products import fix_products

fix_products(self)

prods = self.env['product.product'].search([])
for p in prods: print(p, p.default_code, p.barcode)
len([x for x in prods if x.barcode])
len([x for x in prods if x.default_code])
"""

