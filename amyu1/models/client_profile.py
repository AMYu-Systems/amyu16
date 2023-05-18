from odoo import models, fields, api


class EscalationContact(models.Model):
    _name = "escalation.contact"
    _description = "Escalation Point of Contact"

    level = fields.Selection([('level_1', '1st Level'), ('level_2', '2nd Level'), ('level_3', '3rd Level')],
                             string="Level")
    contact_name = fields.Char(string='Point of Contact', required=True)
    contact_number = fields.Char(string="Contact Number")
    email = fields.Char(string="Email")
    escalation_id = fields.Many2one(comodel_name='client.profile', string="Escalation")


class CorporateOfficer(models.Model):
    _name = "corporate.officer"
    _description = "Corporate Officers"

    name = fields.Char(string='Name', required=True)
    position = fields.Char(string='Position')
    client_profile_ids = fields.Many2one(comodel_name='client.profile', string="Partner")


class ClassOfShares(models.Model):
    _name = 'class.of.shares'
    _description = "Class of Shares"

    class_shares = fields.Char(string="Class of Shares")
    par_value = fields.Float(string="Par Value per Share")
    authorized_no = fields.Float(string="No.")
    authorized_amount = fields.Float(string="Amount")
    subscribed_no = fields.Float(string="No.")
    subscribed_amount = fields.Float(string="Amount")
    treasury_no = fields.Float(string="No.")
    treasury_amount = fields.Float(string="Amount")
    paid_up_no = fields.Float(string="No.")
    paid_up_amount = fields.Float(string="Amount")
    client_share_ids = fields.Many2one(comodel_name='client.profile', string="Class")


class ClientProfile(models.Model):
    _name = 'client.profile'
    _description = "Profile"
    # profile
    assoc_id = fields.Many2one(string="Associate", comodel_name='associates.profile', required=True)
    is_company = fields.Selection([('individual', 'Individual'), ('company', 'Company')], required=True)
    name = fields.Char(string="Client Name", required=True)
    image = fields.Image(string="Image")
    organization_type = fields.Many2one(comodel_name="res.partner.category", string="Organization Type", required=True)
    industry_class = fields.Many2one(comodel_name="res.partner.industry", string="Industry Class", required=True)
    nature_of_business = fields.Text(string="Nature of Activities,Brands,Product & Services")
    date_of_engagement = fields.Date(string="Date", required=True)
    client_id = fields.Char(string="Client ID", required=True)
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

    # Contacts
    unit_no = fields.Char(string="Unit/Floor")
    building_name = fields.Char(string="Building Name")
    street = fields.Char(string="Street")
    district = fields.Char(string="District/Barangay/Village")
    city = fields.Char(string="City")
    zip = fields.Char(string="Zip Code")
    landline = fields.Char(string="Telephone")
    website = fields.Char(string="Website")
    unit_no2 = fields.Char(string="Unit/Floor")
    building_name2 = fields.Char(string="Building Name")
    street2 = fields.Char(string="Street")
    district2 = fields.Char(string="District/Barangay/Village")
    city2 = fields.Char(string="City")
    zip2 = fields.Char(string="Zip Code")
    landline2 = fields.Char(string="Telephone")
    primary_contact_person = fields.Char(string="Primary Contact")
    mobile_no = fields.Char(string="Mobile No.")
    email_address = fields.Char(string="Email Address")
    principal_accounting_officer = fields.Char(string="Principal Accounting Officer")
    landline3 = fields.Char(string="Telephone")
    mobile_no2 = fields.Char(string="Mobile No.")
    email_address2 = fields.Char(string="Email Address")
    corporate_ids = fields.One2many(comodel_name='corporate.officer', inverse_name='client_profile_ids',
                                    string="Corporate Officers")
    # BIR
    vat = fields.Char(string="Tax Id No.")
    rdo_code = fields.Char(string="RDO Code")
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
    ask = fields.Selection([('yes', 'Yes'), ('no', 'No')])
    # SEC/DTI
    registration_number = fields.Char(string="Registration No")
    registration_date_sec = fields.Date('Date')
    trade_name = fields.Char(string="Trade Name")
    date_per_law = fields.Char(string="Date per By-Laws")
    actual_date_meeting = fields.Date('date')
    ask_1 = fields.Selection([('yes', 'Yes'), ('no', 'No')])
    ask_2 = fields.Char(string="If Yes what type of security is the Company permit to sell?")
    class_shares_id = fields.One2many(comodel_name='class.of.shares', inverse_name='client_share_ids',
                                      string="Class of Shares")
    # Regulatory
    ask_3 = fields.Selection([('yes', 'Yes'), ('no', 'No')])
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
    others_reg = fields.Char()
    # SSS
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
    # Escalation
    escalation = fields.One2many(comodel_name='escalation.contact', inverse_name='escalation_id',
                                 string="Escalation Point")
    # client_records
    documents_count = fields.Integer(compute="action_attach_documents")

    def action_attach_documents(self):
        for rec in self:
            rec.documents_count = self.env['client.records'].search_count([
                ('client_profile_id', '=', rec.id)
            ])
        return {
            'type': 'ir.actions.act_window',
            'name': 'Working Papers',
            'res_model': 'client.records',
            'view_mode': 'kanban,form',
            'domain': [('client_profile_id', '=', rec.id)],
            'context': {'default_client_profile_id': rec.id},
            'target': 'current',
        }


class ClientRecords(models.Model):
    _name = 'client.records'
    _rec_name = "file_name"

    upload_file = fields.Binary(string='File', attachment=True)
    file_name = fields.Char(string='Filename')
    client_profile_id = fields.Many2one(string="Client Profile", comodel_name="client.profile")

    @api.model
    def year_selection(self):
        year = 2000  # replace 2000 with your a start year
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


class AssociatesProfile(models.Model):
    _name = 'associates.profile'
    _rec_name = "associates"

    associates = fields.Char(string="Associates")
    associates_image = fields.Image(string="Pictures")
    associates_manager = fields.Char(string="Manager")
    associates_supervisor = fields.Char(string="Supervisor")
    associates_cluster = fields.Char(string="Cluster")
    client_list = fields.One2many(string="List of Clients", comodel_name='associates.profile.lines',
                                  inverse_name='associates_client_list')
    client_ids = fields.One2many(string="Clients", comodel_name='client.profile', inverse_name='assoc_id',
                                 readonly=True)


class AssociatesProfileLines(models.Model):
    _name = 'associates.profile.lines'

    associates_client_list = fields.Many2one(string="Client List", comodel_name='associates.profile')
    # client_id = fields.Many2one(string="Client Information",comodel_name='client.profile')
