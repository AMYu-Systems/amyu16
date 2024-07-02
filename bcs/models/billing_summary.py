from odoo.exceptions import ValidationError
from odoo import fields, models, api
import logging

_logger = logging.getLogger(__name__)


# Test
def test_with_logger(data: any = "Debug Message", warn: bool = False) -> None:
    """
        Outputs a debug message in the odoo log file, 5 times in a row
    """
    method = _logger.info if not warn else _logger.warning
    for _ in range(5):
        method(data)


class BillingSummary(models.Model):
    _name = 'billing.summary'
    _description = "Billing Summary"
    _rec_name = 'client_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _sql_constraints = [
        (
            'unique_client_id',
            'unique(client_id)',
            'Can\'t have duplicate clients.'
        )
    ]

    client_id = fields.Many2one(string="Client Name", comodel_name='client.profile', required=True, tracking=True)

    image_1012 = fields.Image(string="Image")
    partner_id = fields.Many2one(related='client_id.lead_partner_id', string="Partner")
    manager_id = fields.Many2one(related='client_id.manager_id', string="Manager")
    supervisor_id = fields.Many2one(related='client_id.supervisor_id', string="Supervisor")
    associate_id = fields.Many2one(related='client_id.user_id', string="Associate")
    
    service_ids = fields.Many2many(comodel_name='services.type', string="Type of Services")
    audit_ids = fields.One2many(comodel_name='audit.billing', inverse_name='billing_summary_id', string="Audit")
    trc_ids = fields.One2many(comodel_name='trc.billing', inverse_name='billing_summary_id', string="TRC")
    books_ids = fields.One2many(comodel_name='books.billing', inverse_name='billing_summary_id', string="Books")
    permit_ids = fields.One2many(comodel_name='business.permit.billing', inverse_name='billing_summary_id',
                                 string="Business Permit")
    gis_ids = fields.One2many(comodel_name='gis.billing', inverse_name='billing_summary_id', string="GIS")
    loa_ids = fields.One2many(comodel_name='loa.billing', inverse_name='billing_summary_id', string="TXA")
    spe_ids = fields.One2many(comodel_name='special.engagement', inverse_name='billing_summary_id',
                              string="Special Engagement")

    has_aud = fields.Boolean(default=False, tracking=True)
    has_trc = fields.Boolean(default=False, tracking=True)
    has_bks = fields.Boolean(default=False, tracking=True)
    has_per = fields.Boolean(default=False, tracking=True)
    has_gis = fields.Boolean(default=False, tracking=True)
    has_loa = fields.Boolean(default=False, tracking=True)
    has_spe = fields.Boolean(default=False, tracking=True)

    state_selection = [('draft', 'Draft'),
                       ('submitted', 'Submitted'),
                       ('verified', 'Verified'),
                       ('approved', 'Approved')]
    state = fields.Selection(state_selection, default='draft', copy=False)
    
    billing_service_ids = fields.One2many(comodel_name='billing.service', store=True,
                                          inverse_name='billing_summary_id', string="Services")
    
    # # auto create or when "edit -> draft" has been implemented
    # def draft_action(self):
    #     self.state = 'draft'

    # # ops manager press submit
    # def submitted_action(self):
    #     self.state = 'submitted'

    # # fad supervisor press verify
    # def verified_action(self):
    #     self.state = 'verified'

    # # fad manager press approve
    # def approved_action(self):
    #     self.state = 'approved'
    
    
    # Override
    def write(self, vals):
        res = super(BillingSummary, self).write(vals)
        self._oncreate_service_records('AUD', self.audit_ids)
        self._oncreate_service_records('TRC', self.trc_ids)
        self._oncreate_service_records('BKS', self.books_ids)
        self._oncreate_service_records('PER', self.permit_ids)
        self._oncreate_service_records('GIS', self.gis_ids)
        self._oncreate_service_records('TXA', self.loa_ids)
        self._oncreate_service_records('SPE', self.spe_ids)
        return res


    def get_services(self):
        services = self.env['billing.summary'].search([('service_ids', '!=', False)])
        return services


    @api.onchange('service_ids')
    def _onchange_services(self):
        service_list = []
        for service in self.service_ids:
            service_list.append(service.code)
        self.has_aud = 'AUD' in service_list
        self.has_trc = 'TRC' in service_list
        self.has_bks = 'BKS' in service_list
        self.has_per = 'PER' in service_list
        self.has_gis = 'GIS' in service_list
        self.has_loa = 'TXA' in service_list
        self.has_spe = 'SPE' in service_list
        return
    
    
    def _oncreate_service_records(self, service_code:str, service_ids):
        service = self.env['services.type'].search([('code', '=', service_code)], limit=1)
        for rec in service_ids:
            self.create_billing_service(service_type=service, service_record=rec)


    def _onchange_service_records(self, service_code:str, service_ids):
        service = self.env['services.type'].search([('code', '=', service_code)], limit=1)
        actual_service_int_ids = [int(str(serv.id).replace('virtual_', '')) 
                                  for serv in service_ids if str(serv.id).startswith('virtual_')]
        
        
        # Remove deleted ids from the service_ids
        deleted_int_ids = []
        for bserv in self.billing_service_ids:
            bserv_service_id = int(str(bserv.unique_str_id).split('-')[0]) 
            if bserv_service_id not in actual_service_int_ids:
                deleted_int_ids.append(bserv.id)
        for deleted_int_id in deleted_int_ids:
            self.billing_service_ids = [(2, deleted_int_id)]
        
        # Update records from service_ids
        for rec in service_ids:
            self.update_billing_service(service_type=service, service_record=rec)
    
    
    @api.onchange('audit_ids', 'service_ids')
    def _onchange_audit(self):
        self._onchange_service_records('AUD', self.audit_ids)
         
    
    @api.onchange('trc_ids', 'service_ids')
    def _onchange_trc(self):
        self._onchange_service_records('TRC', self.trc_ids)
         
            
    @api.onchange('books_ids', 'service_ids')
    def _onchange_books(self):
        self._onchange_service_records('BKS', self.books_ids)
        
            
    @api.onchange('permit_ids', 'service_ids')
    def _onchange_permit(self):
        self._onchange_service_records('PER', self.permit_ids)
      
            
    @api.onchange('gis_ids', 'service_ids')
    def _onchange_gis(self):
        self._onchange_service_records('GIS', self.gis_ids)
       
            
    @api.onchange('loa_ids', 'service_ids')
    def _onchange_loa(self):
        self._onchange_service_records('TXA', self.loa_ids)
            
            
    @api.onchange('spe_ids', 'service_ids')
    def _onchange_spe(self):
        self._onchange_service_records('SPE', self.spe_ids)
    
    
    def get_services(self):
        services = self.env['billing.summary'].search([('service_ids', '!=', False)])
        return services
    
    
    def get_services_total_amount(self, included_service_ids):
        included = []
        total = 0

        included_code = []
        for service_id in included_service_ids:
            included_code.append(service_id.code)

        if 'AUD' in included_code and self.has_aud: included.append(self.audit_ids)
        if 'TRC' in included_code and self.has_trc: included.append(self.trc_ids)
        if 'BKS' in included_code and self.has_bks: included.append(self.books_ids)
        if 'PER' in included_code and self.has_per: included.append(self.permit_ids)
        if 'GIS' in included_code and self.has_gis: included.append(self.gis_ids)
        if 'TXA' in included_code and self.has_loa: included.append(self.loa_ids)
        if 'SPE' in included_code and self.has_spe: included.append(self.spe_ids)

        for services in included:
            for rec in services:
                total += rec.amount
        return total
    
    
    def get_service_records_as_int_list(self, included_service_ids):
        billing_service_int_ids = []
        for bserv_id in self.billing_service_ids:
            if bserv_id.service_id.id in included_service_ids.ids:
                billing_service_int_ids.append(bserv_id.id)
        return billing_service_int_ids
    
    
    def update_billing_service(self, service_record, service_type):
        '''
        Creates a BillingService record for this BillingSummary if does not exist. 
        Otherwise, add again to table if removed previosly and update the amount if the record exists.
        '''
        # The replace method is absolute bad code, but it works...
        # Onchange only gives a virtual record with id "NewId_<actual_id>" 
        # So we just remove that to query the existing record properly
        unique_id = f'{service_record.id}-{service_type.code}'.replace('NewId_', '')
        existing = self.env['billing.service'].search([('unique_str_id', '=', unique_id)], limit=1)
        
        if existing:
            bserv_included : bool = existing.id in self.billing_service_ids.ids
            # If service not included, remove from billing service table
            if service_type.id not in self.service_ids.ids and bserv_included:
                self.billing_service_ids = [(2, existing.id)]
            else:
                if not bserv_included:
                    # Add to billing service table again if previously removed
                    self.billing_service_ids = [(4, existing.id)]
            # Change amount if edited
            if existing.amount != service_record.amount:
                existing.set_amount(service_record.amount)
                
    
    def create_billing_service(self, service_type, service_record):
        '''
        Creates a BillingService record for this BillingSummary if does not exist. 
        Otherwise, add again to table if removed previosly and update the amount if the record exists.
        '''
        unique_id = f'{service_record.id}-{service_type.code}'
        existing = self.env['billing.service'].search([('unique_str_id', '=', unique_id)], limit=1)
        
        if not existing and service_type.id in self.service_ids.ids:
            # Create new billing service summary
            billing_service_id = self.env['billing.service'].create({
                'billing_summary_id': self.id,
                'unique_str_id': unique_id,
                'service_id': service_type.id,
                'amount': service_record.amount,
            })
            self.billing_service_ids = [(4, billing_service_id.id)]
        
        
        
class BillingService(models.Model):
    _name = 'billing.service'
    _description = "Billing Services"
    # _rec_name = 'name'
    _sql_constraints = [
        (
            'unique_unique_str_id',
            'unique(unique_str_id)',
            'Can\'t have duplicate records.'
        )
    ]
    
    unique_str_id = fields.Char(required=True)
    billing_summary_id = fields.Many2one('billing.summary', ondelete='cascade', required=True)
    
    service_id = fields.Many2one(comodel_name='services.type', required=True)
    service_name = fields.Text(related='service_id.name')
    service_code = fields.Char(related='service_id.code')
    service_str = fields.Char(compute='_compute_service')
    
    amount = fields.Float(required=True)
    
    @api.depends('service_name', 'service_code')
    def _compute_service(self):
        for record in self:
            record.service_str = f'{record.service_name} ({record.service_code})'
            
    # name = fields.Char(readonly=True, compute='_compute_name')
    # @api.depends('service_view', 'amount')
    # def _compute_name(self):
    #     for record in self:
    #         record.name = f'{record.service_view} - PHP {record.amount}'

    def set_amount(self, new_amount:float):
        self.amount = new_amount