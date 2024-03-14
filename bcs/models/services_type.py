from odoo import fields, models


class ServicesType(models.Model):
    _name = 'services.type'
    _description = "Services"

    name = fields.Text(string="Name")
    description = fields.Text(string="Description")
    practice = fields.Selection(
        selection=[('assurance_audit', 'Assurance & Audit'), ('tax_services', 'Tax Services'),
                   ('consultancy_services', 'Consultancy Services'), ('strategy_services', 'Strategy Services')],
        string="Practice")

    active = fields.Boolean(string="Active")
    service_ids = fields.One2many(string="Services", comodel_name='billing.summary', inverse_name="service_ids")
