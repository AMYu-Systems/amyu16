
- Transaction ID : auto sequential with format
- Client id: auto many to one
- [Collection](Collection.md) ids : many to many
- [BillingCollectionUpdates](BillingCollectionUpdates.md) id : one to one
- Date Billed : date
- Last Updated : datetime
- State : auto selection
	- values
		- draft (Ops Manager creates)
		- submitted (Ops Manager to Supervisor)
		- verified (Supervisor to Manager)
		- approved
- Status : selection
	- values
		- not yet sent
		- sent as email
		- sent as errand request
		- client has received
	- constraint : can only be edited once self.state is "approved"
	- maybe has another page where value is False?
	- to easily check if billing is not yet sent to client
	- ***def onchange***
		- if value is "sent as ..." ( or "client has received" ? ) then proceed, else ignore
		- self.date_billed = date.now
		- create new [AccountsReceivable](AccountsReceivable.md)( self : current record, self.amount )
- Other Instructions by ops manager : string?
- Services : preset many to many
	- fetch from [Service](Service.md) (PresetServices)
- Amount : compute
	- models = get models of all self.services
	- // models from [BillingSummary Tables (Engagement)](BillingSummary%20Tables%20(Engagement).md)
	- arjournal = Query [ARJournal](ARJournal.md) according to self.client_id
	- total_amount = arjournal.remaining_balance
	- For billingsummary_model in models
		- client_billsumm = billingsummary_model.filter( client_id = self.client_id ) 
		- amount += sum of all client_billsumm.amount
	- return total_amount
- Issued by : many to one # ops manager
- Remarks : text
	
-  ***Onapprove*** state - once self.state is "Approved"
	- self.billing_updates_id  = create new BillingUpdates( self : current billing ) 
	- Make self.status editable
	
- ***Generate PDF***
	- make SOA and Billing Statement pdf from template


#table