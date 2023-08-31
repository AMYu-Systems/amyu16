from odoo import fields, models


class JobTitle(models.Model):
    _name = 'job.title'
    _description = "Job Details"

    name = fields.Char(string="Work")
    active = fields.Boolean(string="Active", default=True)