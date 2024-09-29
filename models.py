class Incomes:
    """Incomes"""
    def __init__(self, id, amount, date, category):
        self.id = id
        self.amount = amount
        self.date = date
        self.category = category
    
    def __repr__(self):
        return f'Income of amount: {self.amount} on {self.date}'
    
class Expenses:
    """Expenses that the users has to pay, or have paid"""
    def __init__(self, id, amount, category, date, msg=''):
        self.id = id
        self.amount = amount
        self.category = category
        self.date = date
        self.msg = msg
        
    def __repr__(self):
        return f'{self.id}, {self.amount}, {self.category}'
        
class ExpensesCategories:
    """The types of the expenses"""
    def __init__(self, id, description):
        self.id = id
        self.description = description