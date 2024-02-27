
- [Collection](Collection.md) id : many to one
	- Set Collection from submitted
- Client id : many to one
	- Set Client from submitted
- [ARJournal](ARJournal.md) id : many to one
	- Get ARJournal from self.client_id
	- self.arjournal.add_payments_collection( self : current record )
- Journal Index : compute ( self.arjournal.payments_collection_count  + 1 )
- Date Processed : datetime.now
- Amount : float - default=self.collection.amount
	
- ***def set_amount***( num )
	- if self.collection.collection_type is not "Consolidated Payment", ignore
	- self.amount = num 

#table