
# class BaseBilling - not model.Models
- Client : many to one
	- Partner data
	- Manager data
	- Supervisor data
	- Associate data
- Service Fee : float | default=0
- OPE Rate : float | default=0
- OPE : *compute ( **service_fee** * **ope_rate** )*
- VAT : float | default=0.12
- Amount : *compute ( sf + OPE + ((sf + OPE) * vat) )*
- Remarks : text 

# AuditBilling(BaseBilling, models.Model)
- Billing Month : selection(0-11) *# jan-dec*
- Payment Terms : float | default=1 *# 100%, others 50%*
- Details of Service Engagement : text 

# TRCBilling(BaseBilling, models.Model)
- Taxable Reporting Period Start Date
- Taxable Reporting Period End Date
- Tax Reporting Period : date - month year picker ???
- Payment Terms : float | default=1 *# 100%, others 50%*
- Details of Service Engagement : text 

# BooksBilling(BaseBilling, models.Model)
- Billing Month : selection(0-11) *# jan-dec*
- Period Covered : date - month year picker
- No. of Offices or Branches : integer
- Payment Terms : float | default=1 *# 100%, others 50%*
- Reimbursible : float

# BusinessPermitsBilling(BaseBilling, models.Model)
- Billing Month : selection(0-11) *# jan-dec*
- Period Covered : date - month year picker
- No. of Offices or Branches : integer
- Reimbursible : float

# GISBilling(BaseBilling, models.Model)
- Billing Month : selection(0-11) *# jan-dec*
- Details of Service Engagement : text

# LOA Billing(BaseBilling, models.Model)
- Billing Request Date : date
- Payment Terms : float | default=1 *# 1-100%, 0.5-50%*
- Letter Date : date
- Period Covered : date - month year picker
- Details of Service Engagement : text

# SpecialEngagement(BaseBilling, models.Model)
- Billing Month : selection(0-11) *# jan-dec*
- Payment Terms : float | default=1 *# 100%, others 50%*
- Type of Engagement - [SEService](SEService.md) id : many to one
	- many to many? 
	- addable
- Details of Service Engagement : text 

#table