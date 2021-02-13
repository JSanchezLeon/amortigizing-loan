import numpy as np 

class AmortizingLoan():
    def __init__(self, principal, interest, maturity):

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
    
    def print_table(self):
        """Prints a nicely formatted table"""
        print("%-12s%-12s%-12s%-12s%-12s" % ("index","balance","payment","interest","amortization"))
        print("-------------------------------------------------------------")
        for i in self.table["index"]:
            print("%-12i%-12i%-12i%-12i%-12i" % (self.table["index"][i],self.table["balance"][i]\
                ,self.table["payment"][i],self.table["interest"][i],\
                self.table["amortization"][i]))

    
m1 = AmortizingLoan(100000, 0.1/12, 360)

m1.print_table()
print(m1.get_closest_interest_amortization())
print(m1.should_refinance(0.03,12,2466))
print(m1.total_amortization())
print(m1.total_interest())
print(m1.get_interest_as_proportion_principal())


        