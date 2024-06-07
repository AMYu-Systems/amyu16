from odoo import models, fields, api


class ManualPosting(models.TransientModel):
    _name = 'manual.posting'

    collection_id = fields.Many2one(comodel_name='bcs.collection', required=True)
    ar_journal_id = fields.Many2one(comodel_name='soa.ar.journal',
                                    domain="[('id', 'in', context.get('ar_journal_ids', []))]", required=True, )
    manual_amount = fields.Float()
    manual_posting = fields.Boolean(default=True)

    def new_manual_posting(self):
        pc_id = self.ar_journal_id.new_manual_posting(self.collection_id, self.manual_amount)
        self.collection_id.new_manual_posting(pc_id, self.manual_amount)