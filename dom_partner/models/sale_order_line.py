#-*- coding:utf-8 -*-

from openerp import models, fields, api, exceptions, _
from openerp.exceptions import UserError

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'


    dep_id = fields.Many2one(comodel_name='yziact.departement', related='order_partner_id.dep_id', name=u'Département', store=True)
