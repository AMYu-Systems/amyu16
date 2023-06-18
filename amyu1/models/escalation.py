from odoo import models, fields


class EscalationContact(models.Model):
    _name = "escalation.contact"
    _description = "Escalation Point of Contact"

    name = fields.Char(string='Point of Contact')
    level = fields.Selection([('level_1', '1st Level'), ('level_2', '2nd Level'), ('level_3', '3rd Level')],
                             string="Level")
    timeframe = fields.Selection(
        [('lvl1', 'upon encounter of issue; unresolved issue after 1 day; 1 day delay in submission of documents'),
         ('lvl2', 'unresolved issue after 2 days; 2 days delay in submission of documents'),
         ('lvl3', 'unresolved issue after 3 days; 3 days delay in submission of documents')],
        string="Escalation Timeframe")
    contact_number = fields.Char(string="Contact Number")
    email = fields.Char(string="Email Address")
    escalation_id = fields.Many2one(comodel_name='client.profile', string="Escalation")
