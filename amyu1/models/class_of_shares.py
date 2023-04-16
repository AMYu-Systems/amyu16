from odoo import models, fields


class ClassOfShares(models.Model):
    _name = 'class.of.shares'
    _description = "Class of Shares"

    class_shares = fields.Char(string="Class of Shares")
    par_value = fields.Float(string="Par Value per Share")
    authorized_no = fields.Float(string="No.")
    authorized_amount = fields.Float(string="Amount")
    subscribed_no = fields.Float(string="No.")
    subscribed_amount = fields.Float(string="Amount")
    treasury_no = fields.Float(string="No.")
    treasury_amount = fields.Float(string="Amount")
    paid_up_no = fields.Float(string="No.")
    paid_up_amount = fields.Float(string="Amount")
    client_share_ids = fields.Many2one(comodel_name='client.profile', string="Class")
