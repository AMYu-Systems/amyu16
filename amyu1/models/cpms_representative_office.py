from odoo import models, fields, api
from odoo.exceptions import ValidationError


class RepresentativeOffice(models.Model):
    _name = 'representative.office'
    _description = "Representative Office"

    name = fields.Char(string="Country Manager")

    @api.onchange('name')
    def caps_name(self):
        if self.name:
            self.name = str(self.name).title()

    @api.constrains('name')
    def _error_name(self):
        for record in self:
            if any(char.isdigit() for char in record.name):
                raise ValidationError("Numbers are not allowed in this Country Manager Field.")

    asst_manager = fields.Char(string="Asst.Country Manager")

    @api.onchange('asst_manager')
    def caps_asst_manager(self):
        if self.asst_manager:
            self.asst_manager = str(self.asst_manager).title()

    @api.constrains('asst_manager')
    def _error_asst_manager(self):
        for record in self:
            if any(char.isdigit() for char in record.asst_manager):
                raise ValidationError("Numbers are not allowed in this Asst.Country Manager Field.")

    representative_office_id = fields.Many2one(comodel_name='client.profile', string="Representative")
