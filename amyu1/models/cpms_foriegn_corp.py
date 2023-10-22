from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ForeignCorp(models.Model):
    _name = 'foreign.corp'
    _description = "Branch of Foreign Corp"

    name = fields.Char(string="Country Manager")

    @api.onchange('name')
    def caps_name(self):
        if self.name:
            self.name = str(self.name).title()
            for record in self:
                if any(char.isdigit() for char in record.name):
                    raise ValidationError("Numbers are not allowed in this Country Manager Field.")

    asst_manager = fields.Char(string="Asst.Country Manager")

    @api.onchange('asst_manager')
    def caps_asst_manager(self):
        if self.asst_manager:
            self.asst_manager = str(self.asst_manager).title()
            for record in self:
                if any(char.isdigit() for char in record.asst_manager):
                    raise ValidationError("Numbers are not allowed in this Asst.Country Manager Field.")

    foreign_corp_id = fields.Many2one(comodel_name='client.profile', string="Foreign Corporation")
