
from odoo import api, models, fields
import re
import math

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    ref_fourn = fields.Char(compute='_compute_ref_fourn')
    nb_colis = fields.Integer(compute='_compute_nb_colis')

    @api.multi
    def _compute_ref_fourn(self):
        for rec in self:
            m = re.search(r'\[(.*)\]', rec.name)
            try:
                val = m.group(1)
                rec.ref_fourn = val
            except Exception as e:
                rec.ref_fourn = rec.product_id.default_code

    @api.multi
    def _compute_nb_colis(self):
        for rec in self:

            # don't think this can happen, but we never know..
            if not rec.product_id:
                rec.nb_colis = 1
                continue

            # if this is zero, don't divide by zero
            if not rec.product_id.nb_par_colis:
                rec.nb_colis = 1
                continue

            nb_par_colis = rec.product_id.nb_par_colis
            qty = rec.product_qty
            nb = 1
            try :
                nb = math.ceil(qty / nb_par_colis)
            except Exception as e:
                nb = 1

            if nb < 1: nb = 1

            rec.nb_colis = nb

