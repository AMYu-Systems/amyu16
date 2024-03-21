from odoo import fields, models, api
import logging

_logger = logging.getLogger(__name__)

# Test
def test_with_logger(data: any="Debug Message", warn: bool = False) -> None:
    """
        Outputs a debug message in the odoo log file, 5 times in a row
    """
    method = _logger.info if not warn else _logger.warning
    for _ in range(5):
        method(data)

class BillingSummary(models.Model):
    _name = 'billing.summary'
    _description = "Billing Summary"
    _sql_constraints = [
        (
            'unique_name', 
            'unique(name)',
            'Can\'t have duplicate values.'
        )
    ]
    
    client_id = fields.Many2one(string="Client Name", comodel_name='client.profile')
    
    image_1012 = fields.Image(string="Image")
    partner_id = fields.Many2one(related='client_id.lead_partner_id', string="Partner")
    manager_id = fields.Many2one(related='client_id.manager_id', string="Manager")
    supervisor_id = fields.Many2one(related='client_id.supervisor_id', string="Supervisor")
    associate_id = fields.Many2one(related='client_id.user_id', string="Associate")
    service_ids = fields.Many2many(comodel_name='services.type', string="Type of Services")
    audit_ids = fields.One2many(comodel_name='audit.billing', inverse_name='billing_summary_id', string="Audit")
    trc_ids = fields.One2many(comodel_name='trc.billing', inverse_name='billing_summary_id', string="TRC")
    books_ids = fields.One2many(comodel_name='books.billing', inverse_name='billing_summary_id', string="Books")
    permit_ids = fields.One2many(comodel_name='business.permit.billing', inverse_name='billing_summary_id',
                                 string="Business Permit")
    gis_ids = fields.One2many(comodel_name='gis.billing', inverse_name='billing_summary_id', string="GIS")
    loa_ids = fields.One2many(comodel_name='loa.billing', inverse_name='billing_summary_id', string="LOA")
    spe_ids = fields.One2many(comodel_name='special.engagement', inverse_name='billing_summary_id',
                              string="Special Engagement")
    
    has_aud = fields.Boolean(default=False)
    has_trc = fields.Boolean(default=False)
    has_bks = fields.Boolean(default=False)
    has_per = fields.Boolean(default=False)
    has_gis = fields.Boolean(default=False)
    has_loa = fields.Boolean(default=False)
    has_spe = fields.Boolean(default=False)

    def get_services(self):
        services = self.env['billing.summary'].search([('service_ids', '!=', False)])
        return services

    @api.onchange('service_ids')
    def _onchange_services(self):
        service_list = []
        for service in self.service_ids:
            service_list.append(service.code)
        self.has_aud = 'AUD' in service_list
        self.has_trc = 'TRC' in service_list
        self.has_bks = 'BKS' in service_list
        self.has_per = 'PER' in service_list
        self.has_gis = 'GIS' in service_list
        self.has_loa = 'LOA' in service_list
        self.has_spe = 'SPE' in service_list
