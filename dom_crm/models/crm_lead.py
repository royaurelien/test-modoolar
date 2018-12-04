#-*- coding:utf-8 -*-

from odoo import models, fields, api, exceptions, _

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    partner_famille = fields.Many2one(comodel_name="dom.famille", string="Famille client")
    partner_category = fields.Many2many(comodel_name="res.partner.category", string="Etiquettes")
    partner_dep = fields.Many2one(comodel_name="yziact.departement", string="Département")

    def _onchange_partner_id_values(self, partner_id):
        res = super(CrmLead, self)._onchange_partner_id_values(partner_id)

        if partner_id:
            partner_id = self.env['res.partner'].browse(partner_id)

            res.update(
                dict(
                    partner_famille=partner_id.famille.id,
                    partner_category=partner_id.category_id,
                    partner_dep=partner_id.dep_id.id
                )
            )

        return res
