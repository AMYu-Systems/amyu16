from odoo import fields, models, api


class AccountsReceivable(models.Model):
    _name = 'soa.accounts.receivable'
    _description = "Accounts Receivable connected to AR Journal"
    _sql_constraints = [
        (
            'unique_billing_id',
            'unique(billing_id)',
            'Can\'t have duplicate billing_ids.'
        )
    ]
    
    billing_id = fields.Many2one(comodel_name='bcs.billing',  required=True, ondelete='cascade', readonly=True)
    ar_journal_id = fields.Many2one(comodel_name='soa.ar.journal', required=True, ondelete='cascade', readonly=True)
    client_id = fields.Many2one(related='ar_journal_id.client_id', string='Client')
    journal_index = fields.Integer( required=True, readonly=True)
    amount = fields.Float(related='billing_id.amount')
    # amount = fields.Float(compute='_compute_amount')

    # @api.depends("billing_id.amount")
    # def _compute_amount(self):
    #     for record in self:
    #         record.amount = record.billing_id.amount

    name = fields.Char(compute="_compute_name")
    identifier_str = fields.Char(compute="_compute_identifier_str")
    services_str = fields.Char(compute="_compute_services_str")
    service_ids = fields.Many2many(related="billing_id.services_id")
    services_amount = fields.Float(related="billing_id.services_amount")
    previous_amount = fields.Float(related="billing_id.previous_amount")

    @api.depends("identifier_str", "services_str")
    def _compute_name(self):
        for record in self:
            if not record.billing_id: continue
            name = record.identifier_str
            name += ' | ' + record.services_str
            name += ' | ' + f'Previous: {record.previous_amount}'
            record.name = name
    
    @api.depends("billing_id.date_billed")
    def _compute_identifier_str(self):
        for record in self:
            record.identifier_str = str(record.journal_index) \
                + ' | ' + record.billing_id.date_billed.strftime("%b %Y")
        
    @api.depends("service_ids")
    def _compute_services_str(self):
        for record in self:
            amount = '{:,.2f}'.format(record.services_amount)
            services = ''
            for service in record.service_ids:
                services += service.code + ', '
            services = services[:-2] + f' ({amount})'
            record.services_str = services
            
