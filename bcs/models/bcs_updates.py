from odoo import models, fields, api
from datetime import datetime
import pytz


class ForCollectionUpdates(models.Model):
    _name = 'bcs.updates'
    _rec_name = 'billing_id'

    billing_id = fields.Many2one(comodel_name='bcs.billing', string="Billing Transaction", required=True, readonly=True)
    first_followup = fields.Boolean(string='1st Follow-up')
    second_followup = fields.Boolean(string='2nd Follow-up')
    responded = fields.Boolean(string='Responded')
    confirmed_payment = fields.Boolean(string='Confirmed Payment')

    date_first_followup = fields.Datetime(string='Date')
    date_second_followup = fields.Datetime(string='Date')
    date_responded = fields.Datetime(string='Date Responded')
    date_confirmed_payment = fields.Datetime(string='Date Confirmed')
    
    remarks = fields.Text()
    
    # used for view; formatted display
    view_first_followup = fields.Char(string="1st Follow-up")
    view_second_followup = fields.Char(string="2nd Follow-up")
    view_responded = fields.Char(string='Responded')
    view_confirmed = fields.Text(string='Confirmed Payment')
    
    def _update_datetime(self, now):
        if not now:
            return False, ''
        dt = datetime.now()
        return dt, f'{dt.astimezone(pytz.timezone("Asia/Manila")).strftime("%b. %d, %Y | %I:%M %p")}'
    
    @api.onchange('first_followup')
    def _onchange_first_followup(self):
        self.date_first_followup, self.view_first_followup = self._update_datetime(self.first_followup)

    @api.onchange('second_followup')
    def _onchange_second_followup(self):
        self.date_second_followup, self.view_second_followup = self._update_datetime(self.second_followup)

    @api.onchange('responded')
    def _onchange_responded(self):
        self.date_responded, self.view_responded = self._update_datetime(self.responded)

    @api.onchange('confirmed_payment')
    def _onchange_confirmed_payment(self):
        self.date_confirmed_payment, self.view_confirmed = self._update_datetime(self.confirmed_payment)
        self.billing_id.status = 'client_received' if self.confirmed_payment else 'sent_to_client'
        

    # @api.model
    # def create(self, vals):
    #     vals['last_updated'] = fields.Datetime.now()
    #     return super(ForCollectionUpdates, self).create(vals)

    # def write(self, vals):
    #     if vals:
    #         vals['last_updated'] = fields.Datetime.now()
    #     return super(ForCollectionUpdates, self).write(vals)
