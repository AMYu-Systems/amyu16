from odoo import fields, models, api


class AmyuSysIncludedModules(models.Model):
    _name = 'amyusys.included.modules'
    _description = "All modules of AMYU Systems"
    
    name = fields.Char(required=True)
    description = fields.Text()
    module_name = fields.Char(required=True)
    
    