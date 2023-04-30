# from odoo import models, fields
#
#
# class ResPartner(models.Model):
#     _inherit = "res.partner"
#     nature_of_activities = fields.Text(string="Nature of Activities")
#     date_of_engagement = fields.Date('date')
#     unit_no = fields.Char(string="Unit No/Floor No.")
#     building_name = fields.Char(string="Building Name")
#     floor_no = fields.Char(string="Floor No")
#     district = fields.Char(string="District")
#     building_name1 = fields.Char(string="Building")
#     street1 = fields.Char(string="Street")
#     zip_code = fields.Char(string="Zip")
#     city1 = fields.Char(string="City")
#     primary_contact_person = fields.Char(string="Primary Contact Person")
#     mobile_no = fields.Char(string="Mobile No.")
#     email_address = fields.Char(string="Email Address")
#     landline = fields.Char(string="Telephone No.")
#     landline1 = fields.Char(string="Telephone No.")
#     principal_accounting_officer = fields.Char(string="Principal Accounting Officer")
#     mobile_no1 = fields.Char(string="Mobile No.")
#     email_address1 = fields.Char(string="Email Address")
#     landline2 = fields.Char(string="Telephone No.")
#     tax_reporting_compliance = fields.Boolean(string="Tax Reporting & Compliance")
#     annual_registration_update = fields.Boolean(string="Annual Registration Update")
#     agree_upon_procedure = fields.Boolean(string="Agree-Upon Procedures")
#     audit_assurance = fields.Boolean(string="Audit & Assurance")
#     tax_advocacy = fields.Boolean(string="Tax Advocacy(Investigation)")
#     advisory_consultancy = fields.Boolean(string="Advisory & Consultancy")
#     compilation = fields.Boolean(string="Compilation")
#     others = fields.Char(string="Others")
#     rdo_code = fields.Char(string="RDO Code")
#     registration_date = fields.Date('Date')
#     income_tax = fields.Boolean(string="Income Tax")
#     excise_tax = fields.Boolean(string="Excise Tax")
#     value_added_tax = fields.Boolean(string="Value-added Tax")
#     withholding_tax_expanded = fields.Boolean(string="Withholding Tax-Expanded")
#     withholding_tax_compensation = fields.Boolean(string="Withholding Tax-Compensation")
#     registration_fee = fields.Boolean(string="Registration Fee")
#     other_percentage_tax = fields.Char(string="Other Percentage Tax")
#     tax_type = fields.Char(string="Taxpayer Type")
#     invoice_tax = fields.Char(string="Invoice Type")
#     filing_payment = fields.Char(string="Filling & Payment")
#     books_of_account = fields.Char(string="Books of Accounts")
#     psic_psoc = fields.Char(string="PSIC/PSOC")
#     ll_cas_permit_no = fields.Char(string="LL/CAS Permit No")
#     ask = fields.Selection([('yes', 'Yes'), ('no', 'No')])
#     registration_number = fields.Char(string="Registration No")
#     registration_date_sec = fields.Date('Date')
#     trade_name = fields.Char(string="Trade Name")
#     date_per_law = fields.Char(string="Date per By-Laws")
#     actual_date_meeting = fields.Date('date')
#     ask_1 = fields.Selection([('yes', 'Yes'), ('no', 'No')])
#     ask_2 = fields.Char(string="If Yes what type of security is the Company permit to sell?")
#     ask_3 = fields.Selection([('yes', 'Yes'), ('no', 'No')])
#     sss = fields.Char(string="SSS ER No")
#     phic = fields.Char(string="PHIC ER No")
#     hdmf = fields.Char(string="HDMF ER No")
#     sss_filing = fields.Char(string="Filing")
#     phic_filing = fields.Char(string="Filing")
#     hdmf_filing = fields.Char(string="Filing")
#     sss_pay = fields.Char(string="Payment")
#     phic_pay = fields.Char(string="Payment")
#     hdmf_pay = fields.Char(string="Payment")
#     bureau_of_custom = fields.Boolean(string="Bureau of Custom")
#     bangko_sentral_pilipinas = fields.Boolean(string="Bangko Sentral ng Pilipinas")
#     professional_regulation_commission = fields.Boolean(string="Professional Regulation Commission")
#     philippines_council_ngo_certification = fields.Boolean(string="Philippine Council for NGO Certification")
#     cooperative_development_authority = fields.Boolean(string="Cooperative Development Authority")
#     insurance_commission = fields.Boolean(string="Insurance Commission")
#     integrated_bar_philippines = fields.Boolean(string="Integrated Bar of the Philippines")
#     philippines_stock_exchange = fields.Boolean(string="Philippine Stock Exchange")
#     construction_industry_authority_philippines = fields.Boolean(
#         string="Construction Industry authority of the Philippines(PCAB)")
#     philippine_amusement_gaming_corporation = fields.Boolean(string="Philippine Amusement and Gaming Corporation")
#     land_transportation_franchising_regulatory_board = fields.Boolean(
#         string="Land Transportation Franchising and Regulatory Board")
#     others_ri = fields.Char(string="Others")
#     corporate_ids = fields.One2many(comodel_name='corporate.officer', inverse_name='res_ids', string="Officer")
#     share_ids = fields.One2many(comodel_name='class.of.shares', inverse_name='class_ids', string="Shares")
#     escalation = fields.One2many(comodel_name='escalation.contact', inverse_name='escalation_id', string="Escalation Point")
