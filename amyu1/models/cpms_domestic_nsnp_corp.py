from odoo import models, fields


class DomesticCorp(models.Model):
    _name = 'domestic.corp'
    _description = "Domestic NSNP Corp"

    name = fields.Char(string="Chairman of the BOT")
    president = fields.Char(string="President/CEO")
    treasurer = fields.Char(string="Treasurer/CFO")
    corporate_secretary = fields.Char(string="Corporate Secretary")
    vice_chairman = fields.Char(string="Vice-Chairman of the BOT")
    asst_treasurer = fields.Char(string="Asst.Treasurer")
    asst_corp_secretary = fields.Char(string="Asst.Corporate Secretary")
    domestic_corp_id = fields.Many2one(comodel_name='client.profile', string="Domestic NSNP Corporation")
