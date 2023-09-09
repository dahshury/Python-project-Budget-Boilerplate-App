class Category:
    """Complete the Category class in budget.py. It should be able to instantiate objects based on
    different budget categories like food, clothing, and entertainment. When objects are created,
    they are passed in the name of the category. The class should have an instance variable called
    ledger that is a list. The class should also contain the following methods:
    """
    def __init__(self, cat_name) -> None:
        self.cat_name = cat_name
        self.ledger = []
        self.balance = 0.
    def __str__(self) -> str:
        """
        When the budget object is printed it should display:

        A title line of 30 characters where the name of the category is centered in a line of * characters.
        A list of the items in the ledger. Each line should show the description and amount. The first 23
        characters of the description should be displayed, then the amount. The amount should be right aligned,
        contain two decimal places, and display a maximum of 7 characters.
        A line displaying the category total.
        Here is an example of the output:

        *************Food*************
        initial deposit        1000.00
        groceries               -10.15
        restaurant and more foo -15.89
        Transfer to Clothing    -50.00
        Total: 923.96
        """
        # This is an f-string expression. Inside the curly braces, self.cat_name is an attribute or variable that
        # presumably contains a string.
        # The :*^30 part is a formatting specification. It can be broken down as follows:

        # *: This is known as the fill character. In this case, it's an asterisk (*).
        # ^: This is the alignment specifier. It means that the content (in this case, self.name) should be 
        # centered within the available space.
        # 30: This is the width specifier. It specifies the total width of the formatted string.
        
        
        lines = ""
        first_line = f"{self.cat_name:*^30}\n"
        
        for item in self.ledger:
            lines += f"{item['description'][:23]:23}" + f"{item['amount']:>7.2f}\n"

        total_str = "Total: " + str(self.get_balance())
        
        return first_line + lines + total_str

    def deposit(self, amount, description=""):
        
        """
        A deposit method that accepts an amount and description. If no description is given,
        it should default to an empty string. The method should append an object to the ledger 
        list in the form of {"amount": amount, "description": description}.
        """
        
        self.ledger.append({"amount": amount, "description": description})
        
    def withdraw(self, amount, description=""):
        
        """
        A withdraw method that is similar to the deposit method, but the amount passed in should
        be stored in the ledger as a negative number. If there are not enough funds, nothing should
        be added to the ledger. This method should return True if the withdrawal took place, and False
        otherwise.
        """
        if self.check_funds(amount):
            self.ledger.append({"amount": -amount, "description": description})
            return True 
        else:
            return False
    
    def get_balance(self):
        """
        A get_balance method that returns the current balance of the budget category based on the deposits
        and withdrawals that have occurred.
        """
        balance = 0
        for transaction in self.ledger:
            amount = transaction["amount"]
            balance += float(amount)
        return balance
    
    def transfer(self, amount, category):
        """A transfer method that accepts an amount and another budget category as arguments. The method should
        add a withdrawal with the amount and the description "Transfer to [Destination Budget Category]". The 
        method should then add a deposit to the other budget category with the amount and the description
        "Transfer from [Source Budget Category]". If there are not enough funds, nothing should be added to
        either ledgers. This method should return True if the transfer took place, and False otherwise.
        """
        if self.check_funds(amount):
            self.withdraw(amount, f"Transfer to {category.cat_name}")
            category.deposit(amount, f"Transfer from {self.cat_name}")
            return True
        else:
            return False
        
    def check_funds(self, amount):
        if amount > self.get_balance():
            return False
        else:
            return True


def create_spend_chart(categories):
    """Besides the Category class, create a function (outside of the class) called create_spend_chart that takes a list
        of categories as an argument. It should return a string that is a bar chart.

        The chart should show the percentage spent in each category passed in to the function. The percentage spent should
        be calculated only with withdrawals and not with deposits. Down the left side of the chart should be labels 0 - 100.
        The "bars" in the bar chart should be made out of the "o" character. The height of each bar should be rounded down to
        the nearest 10. The horizontal line below the bars should go two spaces past the final bar. Each category name should
        be written vertically below the bar. There should be a title at the top that says "Percentage spent by category".

        This function will be tested with up to four categories.

        Look at the example output below very closely and make sure the spacing of the output matches the example exactly.

        Percentage spent by category
        100|          
         90|          
         80|          
         70|          
         60| o        
         50| o        
         40| o        
         30| o        
         20| o  o     
         10| o  o  o  
          0| o  o  o  
            ----------
             F  C  A  
             o  l  u  
             o  o  t  
             d  t  o  
                h     
                i     
                n     
                g     
            """
            
    title = "Percentage spent by category\n"
    line_creator = []
    bottom_lines = []
    max_letters = 0
    total_withdrawal = sum([item["amount"] for category in categories for item in category.ledger if item["amount"]<0])
    withdrawal_percentage_per_cat={}
    
    for category in categories:
        
        
        if total_withdrawal != 0:
            withdrawal_percentage_per_cat[category] = ((sum([item["amount"] for item in category.ledger if item["amount"] < 0]) / total_withdrawal)* 100 // 10) * 10 
            
        else:
            withdrawal_percentage_per_cat[category] = 0
            
    for i in range(11):
        line_creator.append(str(100-10*i)+"|")
        
        if len(line_creator[i])< 4:
            line_creator[i] = " "*(4-len(line_creator[i])) + line_creator[i]
            
        for j, category in enumerate(categories):
            line_creator[i] += (" "*(1 if j==0 else 2)) +("o" if withdrawal_percentage_per_cat[category] >= (100-(i*10)) else " ")
                                
        line_creator[i] += (" "*2)

        
    top_lines = "\n".join(line_creator) +"\n"
    
    divider = " " * 4 + "-" * (((len(categories)) * 3 ) + 1) +"\n"

    for category in (categories):
        if len(category.cat_name) > max_letters:
            max_letters = len(category.cat_name)
            
    for i in range(max_letters):
        bottom_lines.append((" " * 5))
        for category in categories:
            try:
                bottom_lines[i] += category.cat_name[i] + (" " * 2)
            except:
                bottom_lines[i] += (" " * 3)
                
    bottom_lines = "\n".join(bottom_lines)
    
    return title + top_lines + divider + bottom_lines

    
# Self tests:
food = Category("Food")
entertainment = Category("Entertainment")
business = Category("Business")
food.deposit(900, "deposit")
entertainment.deposit(900, "deposit")
business.deposit(900, "deposit")
food.withdraw(105.55)
entertainment.withdraw(33.40)
business.withdraw(10.99)
create_spend_chart([business, food, entertainment])

        