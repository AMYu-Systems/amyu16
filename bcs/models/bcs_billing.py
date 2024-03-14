import re

from odoo import fields, models, api
from odoo.exceptions import ValidationError


class BcsBilling(models.Model):
    _name = 'bcs.billing'
    _description = "Billing"
    _rec_name = 'client_name'

    transaction = fields.Char(string="Transaction id", readonly="1")

    @api.model
    def create(self, vals):
        name = re.sub(r'\W+', ' ', vals['client_name'])
        name_array = name.split()
        if len(name_array) == 1:
            transaction = name_array[0][0:3]
        elif len(name_array) == 2:
            name1 = name_array[0]
            name2 = name_array[1]
            transaction = (name1[0:2] if len(name1) >= 2 else name1[0:1]) + \
                          (name2[0:2] if len(name1) == 1 else name2[0:1])
        elif len(name_array) >= 3:
            name1 = name_array[0]
            name2 = name_array[1]
            name3 = name_array[2]
            transaction = name1[0:1] + name2[0:1] + name3[0:1]
        # Compute Client ID
        transaction += "-" + self.env['ir.sequence'].next_by_code('billing.id.seq')
        vals['transaction'] = transaction
        return super(BcsBilling, self).create(vals)

    client_name = fields.Char(string="Client Name")
    collection_ids = fields.Many2many(comodel_name='bcs.collection', string="Collection")
    billing_collection_updates = fields.Char(string="Billing Collection Update")
    date_billed = fields.Date(string="Date Billed")
    last_updated = fields.Datetime(string="Last Updated")
    state_selection = [('draft', 'Draft'),
                       ('submitted', 'Submitted'),
                       ('verified', 'Verified'),
                       ('approved', 'Approved')]
    state = fields.Selection(state_selection, default='draft', copy=False)

    # ops manager create
    def draft_action(self):
        self.state = 'draft'

    # ops manager
    def ops_manager_submitted_action(self):
        self.state = 'submitted'

    # fad supervisor
    def fad_supervisor_verified_action(self):
        self.state = 'verified'

    # fad manager
    def fsd_manager_approved_action(self):
        self.state = 'approved'

    status_selection = [('not_sent', 'Not Yet Sent'),
                        ('sent_email', 'Sent As Email'),
                        ('send_errand', 'Send As Errand Request'),
                        ('client_received', 'Client Has Received')]
    status = fields.Selection(status_selection, default='not_sent')

    # @api.constrains('state')
    # def _check_state_for_editing(self):
    #     for record in self:
    #         if record.state == 'approved' and any(
    #                 record[field] != record._origin[field] for field in ['status', 'billing_sent']):
    #             raise ValidationError("Fields can only be edited when state is not 'approved'.")

    other = fields.Text(string="Other Instruction")
    service_id = fields.Many2many(comodel_name="services.type", string="Services")
    amount = fields.Float(string="Amount")
    issued_by = fields.Char(string="Issued By")
    remarks = fields.Text(string="Remarksl")