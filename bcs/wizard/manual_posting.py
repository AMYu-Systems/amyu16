from odoo import models, fields, api


class ManualPosting(models.TransientModel):
    _name = 'manual.posting'

    collection_id = fields.Many2one(comodel_name='bcs.collection', required=True)
    ar_journal_id = fields.Many2one(comodel_name='soa.ar.journal',
                                    domain="[('id', 'in', context.get('ar_journal_ids', []))]", required=True, )
    manual_amount = fields.Float()
    manual_posting = fields.Boolean(default=True)

    def new_manual_posting(self):
        self.env['soa.payments.collection'].create({
            'ar_journal_id': self.ar_journal_id.id,
            'collection_id': self.collection_id.id,
            'manual_amount': self.manual_amount,
            'manual_posting': True,
        })