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

    @api.multi
    def _create_lead_partner_data(self, name, is_company, parent_id=False):
        res = super(CrmLead, self)._create_lead_partner_data(name, is_company, parent_id)

        category_ids = []

        for category in self.partner_category:
            category_ids.append(category.id)

        res.update(
            dict(
                famille=self.partner_famille.id,
                category_id=[(6, 0, category_ids)],
                dep_id=self.partner_dep.id
            )
        )

        return res

    @api.multi
    def action_schedule_meeting(self):
        res = super(CrmLead, self).action_schedule_meeting()

        if self.partner_id:
            if self.partner_id.company_type == 'company':
                res['context']['default_company_activity_id'] = self.partner_id.id
            else:
                if self.partner_id.parent_id:
                    res['context']['default_company_activity_id'] = self.partner_id.parent_id.id
                res['context']['default_contact_activity_id'] = self.partner_id.id

        return res
