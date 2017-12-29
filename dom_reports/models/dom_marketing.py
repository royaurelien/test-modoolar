
from odoo import api, models, fields

PARAMS = [
    ("top_message", "dom.marketing.top_message"),
    ("footer_logo_1", "dom.marketing.footer_logo_1"),
]

class DomMarketing(models.TransientModel):
    _inherit = 'res.config.settings'

    top_message = fields.Binary(string="Message en tête de page")
    footer_logo_1 = fields.Binary(string="Image de pied de page n°1")
    footer_logo_2 = fields.Binary(string="Image de pied de page n°2")
    footer_logo_3 = fields.Binary(string="Image de pied de page n°3")
    footer_logo_4 = fields.Binary(string="Image de pied de page n°4")

    @api.model
    def get_values(self):
        res = super(DomMarketing, self).get_values()
        # use_propagation_minimum_delta=self.env['ir.config_parameter'].sudo().get_param('stock.use_propagation_minimum_delta')
        res.update(
            top_message=self.env['ir.config_parameter'].sudo(
            ).get_param('dom_reports.top_message'),
            footer_logo_1=self.env['ir.config_parameter'].sudo(
            ).get_param('dom_reports.footer_logo_1'),
            footer_logo_2=self.env['ir.config_parameter'].sudo(
            ).get_param('dom_reports.footer_logo_2'),
            footer_logo_3=self.env['ir.config_parameter'].sudo(
            ).get_param('dom_reports.footer_logo_3'),
            footer_logo_4=self.env['ir.config_parameter'].sudo(
            ).get_param('dom_reports.footer_logo_4')
        )
        return res

    @api.multi
    def set_values(self):
        super(DomMarketing, self).set_values()
        #self.env['ir.config_parameter'].sudo().set_param('stock.use_propagation_minimum_delta', self.use_propagation_minimum_delta)
        #""" If we are not in multiple locations, we can deactivate the internal
        #operation types of the warehouses, so they won't appear in the dashboard.
        #Otherwise, activate them.
        #"""

        self.env['ir.config_parameter'].sudo(
        ).set_param('dom_reports.top_message', self.top_message)

        self.env['ir.config_parameter'].sudo(
        ).set_param('dom_reports.footer_logo_1', self.footer_logo_1)
        self.env['ir.config_parameter'].sudo(
        ).set_param('dom_reports.footer_logo_2', self.footer_logo_2)
        self.env['ir.config_parameter'].sudo(
        ).set_param('dom_reports.footer_logo_3', self.footer_logo_3)
        self.env['ir.config_parameter'].sudo(
        ).set_param('dom_reports.footer_logo_4', self.footer_logo_4)

        """
        if self.group_stock_multi_locations:
            warehouses = self.env['stock.warehouse'].search([])
            active = True
        else:
            warehouses = self.env['stock.warehouse'].search([
                ('reception_steps', '=', 'one_step'),
                ('delivery_steps', '=', 'ship_only')])
            active = False
        warehouses.mapped('int_type_id').write({'active': active})
        """
