from odoo import models, fields, api
import re
from odoo.exceptions import ValidationError
from datetime import datetime


class ClientProfile(models.Model):
    _name = 'client.profile'
    _description = "Profile"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Client Name", required=True)
    is_company = fields.Selection([('individual', 'Individual'), ('company', 'Company')], default="company")
    image_101 = fields.Image(string="Image")
    organization_type = fields.Many2one(string="Organization Type", comodel_name="organization.type")
    industry_class = fields.Many2one(string="Industry Class", comodel_name="res.partner.industry")
    nature_of_business = fields.Text(string="Nature of Activities, Brands, Product & Services")
    date_of_engagement = fields.Date(string="Date of Engagement")
    client_system_generated = fields.Char(string="Client ID")
    tax_reporting_compliance = fields.Boolean(string="Tax Reporting & Compliance")
    annual_registration_update = fields.Boolean(string="Annual Registration Update")
    agree_upon_procedure = fields.Boolean(string="Agree-Upon Procedures")
    audit_assurance = fields.Boolean(string="Audit & Assurance")
    tax_advocacy = fields.Boolean(string="Tax Advocacy(Investigation)")
    advisory_consultancy = fields.Boolean(string="Advisory & Consultancy")
    compilation = fields.Boolean(string="Compilation")
    others = fields.Char(string="Others")
    client_record_ids = fields.One2many(string="Client Record", comodel_name="client.records",
                                        inverse_name="client_profile_id")
    state = fields.Selection([('draft', 'Draft'),
                              ('supervisor', 'Supervisor'),
                              ('manager', 'Manager'),
                              ('approved', 'Approved'),
                              ('cancel', 'Returned')], default='draft', string="Status")
    associate_id = fields.Many2one(string="Associate", comodel_name="associates.profile")
    manager_id = fields.Many2one(string="Manager", comodel_name="manager.tags")
    supervisor_id = fields.Many2one(string="Supervisor", comodel_name="supervisor.tags")
    cluster_id = fields.Many2one(string="Cluster", comodel_name="partner.tags")
    state_sequence = fields.Integer(compute='_compute_state_sequence', string='State Sequence', store=True)

    @api.depends('state')
    def _compute_state_sequence(self):
        for record in self:
            if record.state == 'draft':
                record.state_sequence = 1
            elif record.state == 'supervisor':
                record.state_sequence = 2
            elif record.state == 'manager':
                record.state_sequence = 3
            elif record.state == 'approved':
                record.state_sequence = 4
            else:
                record.state_sequence = 0

    def draft_action(self):
        self.state = 'draft'

    def action_submit_supervisor(self):
        self.state = 'supervisor'
        # return {
        #     'name':'Supervisor',
        #     'view_type':'form',
        #     'view_mode':'tree,form',
        #     'res_model':'client.profile',
        #     'type':'ir.actions.act_window',
        #     'target':'inline',
        #     'flags':{'form':{'action_button':True}},
        # }

    def action_approve_supervisor(self):
        self.state = 'manager'

    def action_return(self):
        self.state = 'cancel'

    def action_approve_manager(self):
        self.state = 'approved'
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'Approved',
                'type': 'rainbow_man'
            }
        }

    # @api.onchange("name")
    # def compute_name(self):
    #     client_id = ""
    #     if self.date_of_engagement:
    #         name = re.sub(r'\W+', ' ', self.name)
    #         name_array = name.split()
    #         if len(name_array) == 1:
    #             client_id = name_array[0][0:3]
    #         elif len(name_array) == 2:
    #             name1 = name_array[0]
    #             name2 = name_array[1]
    #             print(name1, name2)
    #             client_id = (name1[0:2] if len(name1) >= 2 else name1[0:1]) + \
    #                         (name2[0:2] if len(name1) == 1 else name2[0:1])
    #         elif len(name_array) >= 3:
    #             name1 = name_array[0]
    #             name2 = name_array[1]
    #             name3 = name_array[2]
    #             client_id = name1[0:1] + name2[0:1] + name3[0:1]
    #
    #         print(client_id.upper())
    def write(self, vals):
        if 'name' in vals:
            old_id = self.client_system_generated.split("-")[0]
            name = re.sub(r'\W+', ' ', vals['name'])
            name_array = name.split()

            if len(name_array) == 1:
                client_system_generated = name_array[0][0:3]
            elif len(name_array) == 2:
                name1 = name_array[0]
                name2 = name_array[1]
                client_system_generated = (name1[0:2] if len(name1) >= 2 else name1[0:1]) + \
                                          (name2[0:2] if len(name1) == 1 else name2[0:1])
            elif len(name_array) >= 3:
                name1 = name_array[0]
                name2 = name_array[1]
                name3 = name_array[2]
                client_system_generated = name1[0:1] + name2[0:1] + name3[0:1]
            vals.update({'client_system_generated': self.client_system_generated.replace(old_id,
                                                                                         client_system_generated).upper()})
        super(ClientProfile, self).write(vals)

    @api.model
    def create(self, vals):
        name = re.sub(r'\W+', ' ', vals['name'])
        name_array = name.split()
        if len(name_array) == 1:
            client_system_generated = name_array[0][0:3]
        elif len(name_array) == 2:
            name1 = name_array[0]
            name2 = name_array[1]
            client_system_generated = (name1[0:2] if len(name1) >= 2 else name1[0:1]) + \
                                      (name2[0:2] if len(name1) == 1 else name2[0:1])
        elif len(name_array) >= 3:
            name1 = name_array[0]
            name2 = name_array[1]
            name3 = name_array[2]
            client_system_generated = name1[0:1] + name2[0:1] + name3[0:1]
        # Compute Client ID
        client_system_generated += "-" + ("0" if int(
            datetime.strftime(datetime.strptime(vals['date_of_engagement'], '%Y-%m-%d'), '%Y')) < 2000 else "1") + \
                                   str(vals['date_of_engagement'])[2:4] + \
                                   str(vals['date_of_engagement'])[5:7] + "-" + \
                                   self.env['ir.sequence'].next_by_code('client.id.seq')

        vals.update({'client_system_generated': client_system_generated.upper()})
        res = super(ClientProfile, self).create(vals)
        if res:
            self.env['escalation.contact'].create({
                'level': 'level_1',
                'timeframe': 'lvl1',
                'escalation_id': res.id
            })
            self.env['escalation.contact'].create({
                'level': 'level_2',
                'timeframe': 'lvl2',
                'escalation_id': res.id
            })
            self.env['escalation.contact'].create({
                'level': 'level_3',
                'timeframe': 'lvl3',
                'escalation_id': res.id
            })
        return res

    unit_no = fields.Char(string="Unit/Floor")
    building_name = fields.Char(string="Building Name")
    street = fields.Char(string="Street")
    district = fields.Char(string="District/Barangay/Village")
    city = fields.Char(string="City")
    zip = fields.Char(string="Zip Code")

    @api.constrains('zip')
    def _validate_zip(self):
        for record in self:
            pattern = r'^\d{4}$'  # Modify the regular expression pattern according to your requirements
            if record.zip and not re.match(pattern, record.zip):
                raise ValidationError('Invalid Zip Code!')

    landline = fields.Char(string="Telephone")

    @api.constrains('landline')
    def _validate_landline(self):
        for record in self:
            pattern = r'^\d{2}-\d{4}-\d{4}\(\d{3}\)$'
            if record.landline and not re.match(pattern, record.landline):
                raise ValidationError('Invalid telephone number format!')

    facsimile_no = fields.Char(string="Facsimile")

    @api.constrains('facsimile_no')
    def _validate_facsimile_no(self):
        for record in self:
            pattern = r'^\d{2}-\d{4}-\d{4}\(\d{3}\)$'
            if record.facsimile_no and not re.match(pattern, record.facsimile_no):
                raise ValidationError('Invalid telephone number format!')

    website = fields.Char(string="Website")
    unit_no2 = fields.Char(string="Unit/Floor")
    building_name2 = fields.Char(string="Building Name")
    street2 = fields.Char(string="Street")
    district2 = fields.Char(string="District/Barangay/Village")
    city2 = fields.Char(string="City")
    zip2 = fields.Char(string="Zip Code")

    @api.constrains('zip2')
    def _validate_zip2(self):
        for record in self:
            pattern = r'^\d{4}$'  # Modify the regular expression pattern according to your requirements
            if record.zip2 and not re.match(pattern, record.zip2):
                raise ValidationError('Invalid Zip Code!')

    landline2 = fields.Char(string="Telephone")

    @api.constrains('landline2')
    def _validate_landline2(self):
        for record in self:
            pattern = r'^\d{2}-\d{4}-\d{4}\(\d{3}\)$'
            if record.landline2 and not re.match(pattern, record.landline2):
                raise ValidationError('Invalid telephone number format!')

    primary_contact_person = fields.Char(string="Primary Contact")
    mobile_number = fields.Char(string="Mobile No.")

    @api.constrains('mobile_number')
    def _validate_mobile_number(self):
        for record in self:
            pattern = r'^(?:\+63|0)\d{10}$'  # Modify the regular expression pattern according to your requirements
            if record.mobile_number and not re.match(pattern, record.mobile_number):
                raise ValidationError('Invalid mobile number format!')

    email_address = fields.Char(string="Email Address")
    principal_accounting_officer = fields.Char(string="Principal Accounting Officer")
    landline3 = fields.Char(string="Telephone")

    @api.constrains('landline3')
    def _validate_landline3(self):
        for record in self:
            pattern = r'^\d{2}-\d{4}-\d{4}\(\d{3}\)$'
            if record.landline3 and not re.match(pattern, record.landline3):
                raise ValidationError('Invalid telephone number format!')

    mobile_number2 = fields.Char(string="Mobile No.")

    @api.constrains('mobile_number2')
    def _validate_mobile_number2(self):
        for record in self:
            pattern = r'^(?:\+63|0)\d{10}$'  # Modify the regular expression pattern according to your requirements
            if record.mobile_number2 and not re.match(pattern, record.mobile_number2):
                raise ValidationError('Invalid mobile number format!')

    email_address2 = fields.Char(string="Email Address")
    corporate_ids = fields.One2many(comodel_name='corporate.officer', inverse_name='client_profile_ids',
                                    string="Corporate Officers")
    vat = fields.Char(string="Tax Id No.")

    @api.constrains('vat')
    def _validate_vat(self):
        for record in self:
            pattern = r'^\d{3}-\d{3}-\d{3}$'  # Modify the regular expression pattern according to your requirements
            if record.vat and not re.match(pattern, record.vat):
                raise ValidationError('Invalid TAX ID!')

    rdo_code = fields.Char(string="RDO Code")

    @api.constrains('rdo_code')
    def _validate_rdo_code(self):
        for record in self:
            pattern = r'^\d{3}$'  # Modify the regular expression pattern according to your requirements
            if record.rdo_code and not re.match(pattern, record.rdo_code):
                raise ValidationError('Invalid RDO Code!')

    registration_date = fields.Date('Date')
    income_tax = fields.Boolean(string="Income Tax")
    excise_tax = fields.Boolean(string="Excise Tax")
    value_added_tax = fields.Boolean(string="Value-added Tax")
    withholding_tax_expanded = fields.Boolean(string="Withholding Tax-Expanded")
    withholding_tax_compensation = fields.Boolean(string="Withholding Tax-Compensation")
    registration_fee = fields.Boolean(string="Registration Fee")
    other_percentage_tax = fields.Boolean(string="Other Percentage Tax")
    other_percentage_tax1 = fields.Char()
    tax_type = fields.Selection([
        ('regular', 'Regular'), ('top_5k_individual', 'Top 5k Individual'), (
            'top_20k_corporate', 'Top 20k Corporate'), ('medium_taxpayer', 'Medium Taxpayer'), (
            'large_taxpayer', 'Large Taxpayer')], string="Taxpayer Type")
    invoice_tax = fields.Selection([
        ('bound_padded', 'Bound(Padded)'), ('computer_aid_loose_leaf', 'Computer-aided(Loose-leaf)'), (
            'cas_generated', 'CAS-Generated')], string="Invoice Type")
    filing_payment = fields.Selection([('ebir_manual', 'eBIR(Manual)'), ('efps', 'EFPS')], string="Filling & Payment")
    books_of_account = fields.Selection(
        [('manual', 'Manual'), ('computer_aid_loose_leaf', 'Computer-aided(Loose-leaf)'),
         ('cas_generated', 'CAS-Generated')], string="Books of Accounts")
    psic_psoc = fields.Char(string="PSIC/PSOC")
    ll_cas_permit_no = fields.Char(string="LL/CAS Permit No")
    ask = fields.Selection([('yes', 'Yes'), ('no', 'No')], default="no")
    registration_number = fields.Char(string="Registration No")
    registration_date_sec = fields.Date('Date')
    trade_name = fields.Char(string="Trade Name")
    date_per_law = fields.Char(string="Date per By-Laws")
    actual_date_meeting = fields.Date('date')
    ask_1 = fields.Selection([('yes', 'Yes'), ('no', 'No')], default="no")
    ask_2 = fields.Text(string="If Yes what type of security is the Company permit to sell?")
    class_shares_id = fields.One2many(comodel_name='class.of.shares', inverse_name='client_share_ids',
                                      string="Class of Shares")
    ask_3 = fields.Selection([('yes', 'Yes'), ('no', 'No')], default="no")
    bureau_of_custom = fields.Boolean(string="Bureau of Customs")
    bangko_sentral_pilipinas = fields.Boolean(string="Bangko Sentral ng Pilipinas")
    professional_regulation_commission = fields.Boolean(string="Professional Regulation Commission")
    philippines_council_ngo_certification = fields.Boolean(string="Philippine Council for NGO Certification")
    cooperative_development_authority = fields.Boolean(string="Cooperative Development Authority")
    insurance_commission = fields.Boolean(string="Insurance Commission")
    integrated_bar_philippines = fields.Boolean(string="Integrated Bar of the Philippines")
    philippines_stock_exchange = fields.Boolean(string="Philippine Stock Exchange")
    construction_industry_authority_philippines = fields.Boolean(
        string="Construction Industry authority of the Philippines(PCAB)")
    philippine_amusement_gaming_corporation = fields.Boolean(string="Philippine Amusement and Gaming Corporation")
    land_transportation_franchising_regulatory_board = fields.Boolean(
        string="Land Transportation Franchising and Regulatory Board")
    others_ri = fields.Boolean(string="Others")
    others_reg = fields.Char(string="Others")
    sss = fields.Char(string="SSS ER No")
    phic = fields.Char(string="PHIC ER No")
    hdmf = fields.Char(string="HDMF ER No")
    sss_filing = fields.Selection([('manual', 'Manual'), ('online', 'Online(AMS-CCL)')], string="Filing")
    phic_filing = fields.Selection([('manual', 'Manual'), ('online', 'Online(ERPS)')], string="Filing")
    hdmf_filing = fields.Selection([('manual', 'Manual'), ('online', 'Online(eSRS)')], string="Filing")
    sss_pay = fields.Selection([('cash', 'Cash'), ('check', 'Check'), ('online_banking', 'Online Banking(EPS)')],
                               string="Payment")
    phic_pay = fields.Selection([('cash', 'Cash'), ('check', 'Check'), ('online_banking', 'Online Banking(EPS)')],
                                string="Payment")
    hdmf_pay = fields.Selection([('cash', 'Cash'), ('check', 'Check'), ('online_banking', 'Online Banking(EPS)')],
                                string="Payment")
    escalation = fields.One2many(comodel_name='escalation.contact', inverse_name='escalation_id',
                                 string="Escalation Point")
    # # client_records
    # documents_count = fields.Integer(compute="action_attach_documents")
    #
    # def action_attach_documents(self):
    #     for rec in self:
    #         rec.documents_count = self.env['client.records'].search_count([
    #             ('client_profile_id', '=', rec.id)
    #         ])
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'name': 'Working Papers',
    #         'res_model': 'client.records',
    #         'view_mode': 'kanban,form',
    #         'domain': [('client_profile_id', '=', rec.id)],
    #         'context': {'default_client_profile_id': rec.id},
    #         'target': 'current',
    #     }

    # # working papers
    # upload_file = fields.Binary(string='File', attachment=True)
    # file_name = fields.Char(string='Filename')
    # year_field = fields.Date(string="Year")


class ClientRecords(models.Model):
    _name = 'client.records'
    _rec_name = "file_name"
    _description = "Records"

    upload_file = fields.Binary(string='File', attachment=True)
    file_name = fields.Char(string='Filename')
    client_profile_id = fields.Many2one(string="Client Profile", comodel_name="client.profile")

    @api.model
    def year_selection(self):
        year = 2000  # replace 2000 with a start year
        year_list = []
        while year != 2030:  # replace 2030 with your end year
            year_list.append((str(year), str(year)))
            year += 1
        return year_list

    year_field = fields.Selection(
        year_selection,
        string="Year",
        default="2023",  # as a default value it would be 2019
    )
