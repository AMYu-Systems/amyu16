from odoo import models, fields, api
from odoo.exceptions import ValidationError


class CapitalizationShare(models.Model):
    _name = 'capitalization.share'
    _description = "Capitalization Shares"

    name = fields.Char(string="Class of Shares")

    @api.onchange('name')
    def caps_name(self):
        if self.name:
            self.name = str(self.name).title()

    @api.constrains('name')
    def _onchange_name(self):
        for record in self:
            if any(char.isdigit() for char in record.name):
                raise ValidationError("Numbers are not allowed in this Field.")

    par_value = fields.Char(string="Par Value per Share")

    @api.constrains('par_value')
    def _check_par_value(self):
        for record in self:
            if record.par_value and not record.par_value.isdigit():
                raise ValidationError("Par Value per Share Field must contain numbers only.")

    # column_3 = fields.Char(string="Authorized")
    authorized_no = fields.Integer(string=" Authorized No.")
    authorized_amount = fields.Float(string="Amount")
    # column_4 = fields.Char(string="Subscribed")
    subscribed_no = fields.Integer(string="Subscribed No.")
    subscribed_amount = fields.Float(string="Amount")
    # column_5 = fields.Char(string="Treasury")
    treasury_no = fields.Integer(string="Treasury No.")
    treasury_amount = fields.Float(string="Amount")
    # column_6 = fields.Char(string="Paid-Up")
    paid_up_no = fields.Integer(string="Paid-Up No.")
    paid_up_amount = fields.Float(string="Amount")
    capitalization_id = fields.Many2one(comodel_name='client.profile', string="Class")
