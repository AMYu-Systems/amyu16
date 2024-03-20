from odoo import fields, models, api


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
    name = fields.Char(string="Client Name")
    image_1012 = fields.Image(string="Image")
    partner = fields.Char(string="Partner")
    manager = fields.Char(string="Manager")
    supervisor = fields.Char(string="Supervisor")
    associate = fields.Char(string="Associate")
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

    def get_services(self):
        services = self.env['billing.summary'].search([('service_ids', '!=', False)])
        return services
