from odoo import fields, models


class PaymentsCollection(models.Model):
    _name = 'soa.payments.collection'
    _description = "Payments Collection connected to AR Journal"
    name = fields.Text(string="Name")
    
    collection_id = fields.Many2one('bcs.collection')
    ar_journal_id = fields.Many2one('soa.ar.journal')
    journal_index = fields.Integer()
    amount = fields.Float()
    
    manual_posting = fields.Boolean(default=False)
    