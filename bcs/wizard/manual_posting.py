from odoo import models, fields, api


class ManualPosting(models.TransientModel):
    _name = 'manual.posting'

    collection_id = fields.Many2one(comodel_name='bcs.collection', required=True)
    ar_journal_id = fields.Many2one(comodel_name='soa.ar.journal',
                                    domain="[('id', 'in', context.get('ar_journal_ids', []))]", required=True, )
    manual_amount = fields.Float()
    manual_posting = fields.Boolean(default=True)

    def new_manual_posting(self):
        client_id = self.ar_journal_id.client_id
        billing_id = self.collection_id.billing_ids.search([('client_id','=',client_id.id)], limit=1)
        pc_id = self.ar_journal_id.new_manual_posting(self.collection_id, billing_id, self.manual_amount)
        self.collection_id.new_manual_posting(billing_id, pc_id, self.manual_amount)