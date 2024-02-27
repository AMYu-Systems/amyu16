Onsubmit of Billing, process a new record.

- [Billing](Billing.md) id : many to one
	- Set Billing from submitted
- Client id : many to many
	- Set Client from submitted 
- [ARJournal](ARJournal.md) id : many to one
	- Query ARJournal from self.billing.client
	- self.arjournal.add_accounts_receivable( self : current record )
- Journal Index : compute ( self.arjournal.accounts_receivable_count  + 1)
- Date Processed : datetime.now
- Amount : self.billing.amount

#table
