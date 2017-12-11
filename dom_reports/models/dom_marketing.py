
from odoo import api, models, fields

PARAMS = [
    ("top_message", "dom.marketing.top_message"),
    ("footer_logo_1", "dom.marketing.footer_logo_1"),
]

class DomMarketing(models.TransientModel):
    _inherit = 'res.config.settings'

    top_message = fields.Html(string="Message en tête de page")
    footer_logo_1 = fields.Binary(string="footer logo 1")

    @api.model
    def get_values(self):
        res = super(DomMarketing, self).get_values()
        # use_propagation_minimum_delta=self.env['ir.config_parameter'].sudo().get_param('stock.use_propagation_minimum_delta')
        res.update(
            top_message=self.env['ir.config_parameter'].sudo(
            ).get_param('dom_reports.top_message')
        )
        res.update(
            footer_logo_1=self.env['ir.config_parameter'].sudo(
            ).get_param('dom_reports.footer_logo_1')
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
