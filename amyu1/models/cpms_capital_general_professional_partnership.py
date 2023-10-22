from odoo import models, fields, api
from odoo.exceptions import ValidationError


class CapitalGeneralProfessionalPartnership(models.Model):
    _name = 'capital.general.professional.partnership'
    _description = "Capital General Partnership"

    name = fields.Char(string="Partner")

    @api.onchange('name')
    def caps_name(self):
        if self.name:
            self.name = str(self.name).title()
            for record in self:
                if any(char.isdigit() for char in record.name):
                    raise ValidationError("Numbers are not allowed in Partner Field.")

    capital_contribution_amount = fields.Float(string="Capital Contribution Amount")
    capital_general_professional_partner_id = fields.Many2one(comodel_name='client.profile',
                                                              string="Capital Contribution Amount")
