class Account:
    def __init__(self,account,balance=0):
        self.account=account
        self.balance=balance
    
    def add(self,addend):
        self.balance=int(self.balance)+int(addend)
    
    def withdraw(self,subtrahend):
        balance=int(self.balance)-int(subtrahend)
        if(balance>=0):
            self.balance=balance
        else:
            raise ValueError("Insufficient Balance")
    
    def get_balance(self):
        return self.balance
    
    def __str__(self):
        return self.account