# In order to access and change data on a spreadsheet, import the gspread library.
import gspread

# For authentication, import the Credentials class.
from google.oauth2.service_account import Credentials

# Scope constant for IAM.
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

# Authenticate and create the gspread client
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('Personal_Financial_Plan').sheet1


class FinancialTracker:
    """
    This class contains all of the logic needed to manage a financial tracker, including how to set income, 
    add expenses, compute totals, and work with a worksheet.
    """
    def __init__(self, worksheet):
        """
        It gets triggered whenever a new class instance is made. Along with 'self', it requires one parameter 'worksheet'.
        """
        self.income = 0
        self.expenses = []
        self.worksheet = worksheet
        self.load_from_sheet()

    def set_income(self, amount):
        """
        The process determines whether the amount passed is less than zero.
        A ValueError with the message "Income cannot be less than 0" is raised if the amount is negative. 
        This guarantees that there is no way to set the revenue to a negative amount.
        """
        if amount < 0:
            raise ValueError("Income cannot be less than 0.")
        self.income = amount
        self.worksheet.update('A2', self.income)

    def add_expense(self, description, amount, category):
        """
        Determines whether the cost is negative and raises an error if it is.
        Provides the description, amount, and category of the item
        adds a new row to a worksheet (self.worksheet) with the expense details.
        """
        if amount < 0:
            raise ValueError("Expense amount cannot be less than 0.")
        self.expenses.append({"description": description, "amount": amount, "category": category})
        self.worksheet.append_row(['', description, amount, category])

    def total_expenses(self):
        """
        Computes the total expenses by summing the amounts of all expenses in the list.
        """
        return sum(expense["amount"] for expense in self.expenses)

    def calculate_remaining_balance(self):
        """
        Calculates the remaining balance by subtracting total expenses from income.
        """
        return self.income - self.calculate_total_expenses()
    
    def display_summary(self):
        """
        It consists of total amount earned, a list of all the expenses, including information on the type, amount, and description of each expense.
        Total cost, remaining amount following the subtraction of all costs from all revenue.
        """
        print("\n---- Monthly Personal Finances Summary ----")
        print(f"Total Income: ${self.income:.2f}")
        print("Expenses:")
        for expense in self.expenses:
            print(f" - {expense['description']} ({expense['category']}): ${expense['amount']:.2f}")
        print(f"Total Expenses: ${self.total_expenses():.2f}")
        print(f"Remaining Balance: ${self.calculate_remaining_balance():.2f}")