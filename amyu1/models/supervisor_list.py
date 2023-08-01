from odoo import models, fields


class SupervisorTags(models.Model):
    _name = 'supervisor.tags'
    _rec_name = "supervisor_id"
    _description = "Supervisor Tags"

    supervisor_id = fields.Char(string="Supervisor")
    active = fields.Boolean(string="Active",default=True)
