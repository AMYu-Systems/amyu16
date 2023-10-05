from odoo import models, fields, api
from odoo.exceptions import ValidationError


class DomesticCorp(models.Model):
    _name = 'domestic.corp'
    _description = "Domestic NSNP Corp"

    name = fields.Char(string="Chairman of the BOT")

    @api.onchange('name')
    def caps_name(self):
        if self.name:
            self.name = str(self.name).title()

    @api.constrains('name')
    def _onchange_name(self):
        for record in self:
            if any(char.isdigit() for char in record.name):
                raise ValidationError("Numbers are not allowed in Chairman of the BOT Field.")

    president = fields.Char(string="President/CEO")

    @api.onchange('president')
    def caps_president(self):
        if self.president:
            self.president = str(self.president).title()

    @api.constrains('president')
    def _onchange_president(self):
        for record in self:
            if any(char.isdigit() for char in record.president):
                raise ValidationError("Numbers are not allowed in President/CEO Field.")

    treasurer = fields.Char(string="Treasurer/CFO")

    @api.onchange('treasurer')
    def caps_treasurer(self):
        if self.treasurer:
            self.treasurer = str(self.treasurer).title()

    @api.constrains('treasurer')
    def _onchange_treasurer(self):
        for record in self:
            if any(char.isdigit() for char in record.treasurer):
                raise ValidationError("Numbers are not allowed in Treasurer/CFO Field.")

    corporate_secretary = fields.Char(string="Corporate Secretary")

    @api.onchange('corporate_secretary')
    def caps_corporate_secretary(self):
        if self.corporate_secretary:
            self.corporate_secretary = str(self.corporate_secretary).title()

    @api.constrains('corporate_secretary')
    def _onchange_corporate_secretary(self):
        for record in self:
            if any(char.isdigit() for char in record.corporate_secretary):
                raise ValidationError("Numbers are not allowed in Corporate Secretary Field.")

    vice_chairman = fields.Char(string="Vice-Chairman of the BOT")

    @api.onchange('vice_chairman')
    def caps_vice_chairman(self):
        if self.vice_chairman:
            self.vice_chairman = str(self.vice_chairman).title()

    @api.constrains('vice_chairman')
    def _onchange_vice_chairman(self):
        for record in self:
            if any(char.isdigit() for char in record.vice_chairman):
                raise ValidationError("Numbers are not allowed in Vice-Chairman of the BOT Field.")

    asst_treasurer = fields.Char(string="Asst.Treasurer")

    @api.onchange('asst_treasurer')
    def caps_asst_treasurer(self):
        if self.asst_treasurer:
            self.asst_treasurer = str(self.asst_treasurer).title()

    @api.constrains('asst_treasurer')
    def _onchange_asst_treasurer(self):
        for record in self:
            if any(char.isdigit() for char in record.asst_treasurer):
                raise ValidationError("Numbers are not allowed in Asst.Treasurer Field.")

    asst_corp_secretary = fields.Char(string="Asst.Corporate Secretary")

    @api.onchange('asst_corp_secretary')
    def caps_asst_corp_secretary(self):
        if self.asst_corp_secretary:
            self.asst_corp_secretary = str(self.asst_corp_secretary).title()

    @api.constrains('asst_corp_secretary')
    def _onchange_asst_corp_secretary(self):
        for record in self:
            if any(char.isdigit() for char in record.asst_corp_secretary):
                raise ValidationError("Numbers are not allowed in Asst.Corporate Secretary Field.")

    domestic_corp_id = fields.Many2one(comodel_name='client.profile', string="Domestic NSNP Corporation")
