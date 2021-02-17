import python.mortgage.AmortizingLoan
import random

class ABS():
    def __init__(self, n_loans, min_balance, max_balance):
        self.n_loans = n_loans
        self.min = min_balance
        self.max = max_balance
        self.balances = [random.randint(self.min,self.max) for loan in range(self.n_loans)]
        self.asset_prices = [balances - random.randint(10e3,20e3) for balances in self.balances]
        self.maturities = [random.choice([15,30]) for maturity in range(self.n_loans)]
        self.interests = [random.randint(3,11)/100 for rate in range(self.n_loans)]

    
    def generate_pool(self):
        loans = list(zip(self.asset_prices,self.balances,self.interests,self.maturities))
        pool = [AmortizingLoan(loan[0], loan[1], loan[2], loan[3]) \
            for loan in loans]
        self.pool = pool
        return self.pool

abs1 = ABS(10, 10e4, 20e4)
print(abs1.generate_pool())

    
        