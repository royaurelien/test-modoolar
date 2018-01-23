#-*- coding:utf-8 -*-

from odoo import models, fields, api, exceptions, _
from odoo.tools.safe_eval import safe_eval
from odoo.exceptions import UserError, ValidationError



class DepartementDeliveryRule(models.Model):
    _inherit = 'delivery.price.rule'

    #### SELECTION ####
    localisation = fields.Selection(selection=[('zone','Zone'), ('dep', u'Département')], default='zone')


    #### RELATION ####
    dep_ids = fields.Many2many(comodel_name='yziact.departement', string=u"Département")
    zone_id = fields.Many2one(comodel_name='dom.zone', string="Zone")


class DepartementProviderGrid(models.Model):
    _inherit = 'delivery.carrier'

    def get_zone(self):
        pass

    def get_dep(self):
        pass

    def _get_price_available(self, order):
        self.ensure_one()


        total = weight = volume = quantity = 0
        total_delivery = 0.0
        zone = False
        dep = False

        if order and order.partner_shipping_id.id:
            shipping = order.partner_shipping_id
            dep = shipping.dep_id
            zone = dep.zone_id

        for line in order.order_line:
            if line.state == 'cancel':
                continue
            if line.is_delivery:
                total_delivery += line.price_total
            if not line.product_id or line.is_delivery:
                continue
            qty = line.product_uom._compute_quantity(line.product_uom_qty, line.product_id.uom_id)
            weight += (line.product_id.weight or 0.0) * qty
            volume += (line.product_id.volume or 0.0) * qty
            quantity += qty
        total = (order.amount_total or 0.0) - total_delivery

        total = order.currency_id.with_context(date=order.date_order).compute(total, order.company_id.currency_id)

        return self._get_price_from_picking(total, weight, volume, quantity, zone, dep)


    def _get_price_from_picking(self, total, weight, volume, quantity, zone=False,dep=False):
        price = 0.0
        criteria_found = False
        price_dict = {'price': total, 'volume': volume, 'weight': weight, 'wv': volume * weight, 'quantity': quantity, 'zone_id':zone,'dep_ids':dep}
        for line in self.price_rule_ids:
            test = safe_eval(line.variable + line.operator + str(line.max_value), price_dict)
            if line.localisation == 'zone':
                if zone  != line.zone_id:
                    continue
            else :
                if not dep in line.dep_ids:
                    continue

            if test:
                price = line.list_base_price + line.list_price * price_dict[line.variable_factor]
                criteria_found = True
                break
        if not criteria_found:
            raise UserError(_("No price rule matching this order; delivery cost cannot be computed."))

        return price
