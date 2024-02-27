
- Client : many to one
- [AccountsReceivable](AccountsReceivable.md) ids : many to many
- [PaymentsCollection](PaymentsCollection.md) ids : many to many
- AccountsReceivableCount : compute ( num items of self.accounts_receivable )
- PaymentsCollectionCount : compute ( num items of self.payments_collection )
- Last Updated : datetime
- Initial Balance : float
- Balance :  float
	
- ***def add_accounts_receivable ( AccountsReceivable )***
	- self.accounts_receivable.add( AccountsReceivable )
	- self.balance += AccountsReceivable.amount
	
- ***def add_payments_collection ( PaymentsCollection )***
	- self.accounts_receivable.add( PaymentsCollection )
	- self.balance -= PaymentsCollection.amount
	
- ***def set_initial_balance ( float )***
	- if self.balance != 0, ignore or return error prompt
	- self.intial_balance = self.balance = float
	
- ***def check_balance_with_records***
	- amount = All accounts_receivable_ids.amount - All payments_collection_ids.amount
	- if self.balance != amount
		- difference = absolute_value( amount - self.balance )
		- "There is a {difference} pesos amount difference."
		- if difference is same as self.initial_balance
			- "The difference is equal to the amount of the inputted initial balance"
		- else, implementation error?

#table