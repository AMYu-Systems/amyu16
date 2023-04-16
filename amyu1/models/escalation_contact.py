from odoo import models, fields


class EscalationContact(models.Model):
    _name = "escalation.contact"
    _description = "Escalation Point of Contact"

    name = fields.Char(string='Escalation Point of Contact', required=True)
    number_email = fields.Char(string="Contact Number and Email")
    escalation_id = fields.Many2one(comodel_name='client.profile', string="Escalation")
