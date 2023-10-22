from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SoleProprietor(models.Model):
    _name = 'sole.proprietor'
    _description = "Sole Proprietor"

    name = fields.Char(string='Proprietor/Proprietress')

    @api.onchange('name')
    def caps_name(self):
        if self.name:
            self.name = str(self.name).title()
            for record in self:
                if any(char.isdigit() for char in record.name):
                    raise ValidationError("Numbers are not allowed in this Proprietor/Proprietress Field.")

    sole_proprietor_id = fields.Many2one(comodel_name='client.profile', string="Proprietor/Proprietress")
