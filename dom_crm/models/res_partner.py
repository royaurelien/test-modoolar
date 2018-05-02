#-*- coding:utf-8 -*-

from odoo import models, fields, api, exceptions, _
from datetime import datetime


class ResPartner(models.Model):
    _inherit = 'res.partner'

    CA_objectif = fields.Float('CA Objectif')
    CA_progress = fields.Integer('progess', compute='_compute_ca_progress')



    @api.multi
    def _compute_ca_progress(self):
        for partner in self :
            objective = partner.CA_objectif
            real = partner.ca_12

            if str(objective) == '0.0' or str(real) == '0.0':
                progress = 0
            else:

                progress = int(100.0 * real / objective)

            partner.CA_progress = progress


    #### OVERWRITE ####
    def _compute_sale_order_count(self):
        year = datetime.now().year
        sale_data = self.env['sale.order'].read_group(domain=[('partner_id', 'child_of', self.ids), ('confirmation_date','ilike','%'+str(year)+'%')],
                                                      fields=['partner_id'], groupby=['partner_id'])
        print("sale_data", sale_data)
        # read to keep the child/parent relation while aggregating the read_group result in the loop
        partner_child_ids = self.read(['child_ids'])
        mapped_data = dict([(m['partner_id'][0], m['partner_id_count']) for m in sale_data])
        for partner in self:

            # let's obtain the partner id and all its child ids from the read up there
            item = next(p for p in partner_child_ids if p['id'] == partner.id)
            partner_ids = [partner.id] + item.get('child_ids')
            # then we can sum for all the partner's child
            partner.sale_order_count = sum(mapped_data.get(child, 0) for child in partner_ids)
