import logging, pytz, datetime, pandas, math
from odoo import api, fields, models

class Liaison(models.Model):
    _name = 'liaison'
    _description = 'Liaison Record for the errands'

    user = fields.Many2one('res.users')
    assigned_location = fields.Many2one('location')
    name = fields.Char(compute="_compute_name", string="Displayed Name", readonly=True)
    
    @api.depends("user.name")
    def _compute_name(self):
        for record in self:
            record.name = record.user.name