import numpy as np 
import random

class AmortizingLoan():
    def __init__(self, asset_price, principal, interest, maturity):

        self.asset_price = asset_price
        self.principal = principal
        self.interest = interest
        self.maturity = maturity
        self.index = range(self.maturity+1)
        self.payment = self.get_payment()
        self.table = self.generate_amortization_table()
    
    def get_payment(self):
        """ 
        Calculates loan payment
        """
        sum_factor = float()
        for n in self.index[1:]:
            sum_factor += 1/(1+self.interest)**n
        return self.principal/sum_factor
    
    def get_LTV(self):
        return self.principal/self.asset_price
    
    def generate_amortization_table(self):
        """
        Generates dictionary that contains all the core information
        about the loan amortization, interest payments, periods, 
        and remaining balance
        """
        payment = self.payment
        self.table = {"index":[index for index in self.index],\
            "payment": [payment for n in self.index],
            "interest":[0],
            "amortization":[0],
            "balance":[self.principal]}
        for i in self.table["index"][1:]:
            interest = self.table["balance"][i-1] * self.interest
            self.table["interest"].append(round(interest,0))
            amortization = payment - interest
            self.table["amortization"].append(round(amortization,0))
            prior_balance = self.table["balance"][i-1] 
            ending_balance = prior_balance - amortization
            self.table["balance"].append(round(ending_balance,0))

        return self.table

    def total_amortization(self):
        """
        Sums all the mortgage amortization. 
        It should add to the total principal, but currently
        the calculation is off
        """
        return sum(self.table["amortization"])

    
    def total_interest(self):
        """
        Returns the sum of all the interest paid over
        the lifetime of the loan
        """
        return sum(self.table["interest"])
    
    def get_interest_as_proportion_principal(self):
        return self.total_interest()/self.principal
    
    def get_max_interest(self):
        """
        Function return year where max interest is paid
        Usually the max ammount of interest in paid on Y1
        But there are some instances where this might chance
        """
        max_int = max(self.table["interest"])
        print(max_int)
        for index in self.table["index"]:
            if self.table["interest"][index] == max_int:
                return index
        
    def get_closest_interest_amortization(self):
        """
        Return the period on which the interest poayment is 
        closest to the loan amortization
        """
        differences = [abs(self.table["interest"][i] - self.table["amortization"][i])\
            for i in self.table["index"][1:]]
        min_diff = min(differences)
        return differences.index(min_diff) + 1
    
    def should_refinance(self, new_interest, current_n, costs):
        """
        Return wether or not a loan should be refinance based on:
        -new interest rate
        -current_n = time lapsed since loan origination 
        -cost = the total cost of originating a new lona (title insurance,etc)
        """
        current_payment = self.payment
        current_interest = self.interest
        fv_after_current_n = np.fv(current_interest,current_n,-current_payment,\
            self.principal)
        payment_after_refinancing = np.pmt(new_interest, self.maturity - current_n, -fv_after_current_n )
        payment_difference =  - current_payment - payment_after_refinancing
        irr = np.rate(self.maturity-current_n, -payment_difference, -costs, 0)
        if irr > new_interest:
            return True
        else:
            return False
            
    def get_duration_dispersion_convexity(self,periods=1, current_period = 0):
        """
        Computes duration and convexity using loan cashflows.
        At the moment this is not accounting for prepayments
        """ 
        discounted_cashflow = [self.payment/(1+self.interest)**i for i in self.index[current_period:]]
        discount_sum = sum(discounted_cashflow)
        weight = [cf/discount_sum for cf in discounted_cashflow]
        time_weight = [weight[i] * i for i in range(1,len(weight))]
        sum_time_weight = sum(time_weight)
        dispersion_array = [((i - sum_time_weight)**2)*weight[i] for i in range(1,len(weight))]
        dispersion_statistic = sum(dispersion_array)
        cashflow_yield = np.irr([-self.table["balance"][current_period]] + [self.payment] * (self.maturity - current_period))
        convexity_array = [i * (i+1) * weight[i] for i in range(1,len(weight))]
        convexity_statistic = sum(convexity_array)/(1+cashflow_yield)**2
        convexity = (sum_time_weight ** 2 + sum_time_weight + dispersion_statistic)/(1+cashflow_yield)**2
        
        return {"duration":sum_time_weight/periods,\
            "dispersion":dispersion_statistic/periods,\
                "convexity":convexity_statistic/periods}

    
    def print_table(self):
        """Prints a nicely formatted table"""
        print("%-12s%-12s%-12s%-12s%-12s" % ("index","balance","payment","interest","amortization"))
        print("-------------------------------------------------------------")
        for i in self.table["index"]:
            print("%-12i%-12i%-12i%-12i%-12i" % (self.table["index"][i],self.table["balance"][i]\
                ,self.table["payment"][i],self.table["interest"][i],\
                self.table["amortization"][i]))


asset_price = 345000
loan = 325000
rate = 0.1/12
maturity = 12*30
m1 = AmortizingLoan(asset_price,loan, rate, maturity)

m1.print_table()
print(m1.get_closest_interest_amortization())
print(m1.should_refinance(0.03/12,24,2466))
print(m1.total_amortization())
print(m1.total_interest())
print(m1.get_interest_as_proportion_principal())
print(m1.get_duration_dispersion_convexity(periods=12,current_period = 180))
print(m1.get_LTV())



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
#print(abs1.calculate_abs_cashflows())


        