from odoo import models, fields, api
from odoo.exceptions import ValidationError


class GeneralProfessionalPartnership(models.Model):
    _name = 'general.professional.partnership'
    _description = "General Professional Partnership"

    name = fields.Char(string="Managing Partner")

    @api.onchange('name')
    def caps_name(self):
        if self.name:
            self.name = str(self.name).title()

    @api.constrains('name')
    def _error_name(self):
        for record in self:
            if any(char.isdigit() for char in record.name):
                raise ValidationError("Numbers are not allowed in this Managing Partner Field.")

    partner = fields.Char(string="Partner")

    @api.onchange('partner')
    def caps_partner(self):
        if self.partner:
            self.partner = str(self.partner).title()

    @api.constrains('partner')
    def _error_partner(self):
        for record in self:
            if any(char.isdigit() for char in record.partner):
                raise ValidationError("Numbers are not allowed in this Partner Field.")

    general_professional_partnership_id = fields.Many2one(comodel_name='client.profile', string="Professional")
