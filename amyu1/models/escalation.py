from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re


class EscalationContact(models.Model):
    _name = "escalation.contact"
    _description = "Escalation Point of Contact"

    name = fields.Char(string='Point of Contact')

    @api.onchange('name')
    def caps_name(self):
        if self.name:
            self.name = str(self.name).title()

    @api.constrains('name')
    def _error_name(self):
        for record in self:
            if any(char.isdigit() for char in record.name):
                raise ValidationError("Numbers are not allowed in Point of Contact Field.")

    level = fields.Selection([('level_1', '1st Level'), ('level_2', '2nd Level'), ('level_3', '3rd Level')],
                             string="Level")
    timeframe = fields.Selection(
        [('lvl1', 'upon encounter of issue; unresolved issue after 1 day; 1 day delay in submission of documents'),
         ('lvl2', 'unresolved issue after 2 days; 2 days delay in submission of documents'),
         ('lvl3', 'unresolved issue after 3 days; 3 days delay in submission of documents')],
        string="Escalation Timeframe")
    contact_number = fields.Char(string="Contact Number")

    @api.constrains('contact_number')
    def _validate_contact_number(self):
        for record in self:
            pattern = r'^(?:\+63|0)\d{10}$'  # Modify the regular expression pattern according to your requirements
            if record.contact_number and not re.match(pattern, record.contact_number):
                raise ValidationError('Invalid Escalation Matrix Contact Number format!')

    email = fields.Char(string="Email Address")

    @api.constrains('email')
    def _check_email_format(self):
        for record in self:
            if record.email and '@' not in record.email:
                raise ValidationError("Invalid email address")

    escalation_id = fields.Many2one(comodel_name='client.profile', string="Escalation")