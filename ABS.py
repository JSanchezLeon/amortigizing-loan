"""
    Create prototype for ABS class that uses AmortizingLoan class
    -NOT CURRENTLY WORKING, THE CLASS BELOW IS STILL IN DEVELOPMENT
"""
import random
from  AmortizingLoan import AmortizingLoan

class ABS():
    def __init__(self, n_loans, min_balance, max_balance):
        self.n_loans = n_loans
        self.min = min_balance
        self.max = max_balance
        self.balances = [random.randint(self.min,self.max) for loan in range(self.n_loans)]
        self.asset_prices = [balances + random.randint(10e3,20e3) for balances in self.balances]
        self.maturities = [random.choice([15*12,30*12]) for maturity in range(self.n_loans)]
        self.interests = [random.randint(3,11)/100 for rate in range(self.n_loans)]

    def __str__(self):
        return "number of loans is {}".format(self.n_loans)

    def generate_pool(self):
        loans = list(zip(self.asset_prices,self.balances,self.interests,self.maturities))
        pool = [AmortizingLoan(loan[0], loan[1], loan[2], loan[3]) \
            for loan in loans]
        self.pool = pool
        return self.pool
    
    def print_payments(self):
        for i in self.pool:
            print(i.get_payment())
        return 

    def calculate_abs_cashflows(self):
        self.cashflow, self.ltv, self.total_balance, self.wam, self.wac = 0, 0, 0, 0, 0
        for loan in self.pool:
            self.cashflow += loan.get_payment()
            self.ltv += loan.get_LTV() * (1/self.n_loans)
            self.total_balance += loan.principal
        for loan in self.pool:
            self.wam += loan.maturity * (loan.principal/self.total_balance)
            self.wac += loan.interest * (loan.principal/self.total_balance)
    
        return self.cashflow, self.ltv, self.total_balance, self.wam, self.wac



abs1 = ABS(int(10e3), 10e4, 20e4)
abs1.generate_pool()
print(abs1.calculate_abs_cashflows())

