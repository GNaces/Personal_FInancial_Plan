import json

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
    
    def load_from_sheet(self):
        """
        This method is useful for initializing a FinancialTracker instance with previously saved financial data from a Google Sheet, 
        allowing the program to continue working with previously entered income and expense data.
        """
        try:
            income_value = self.worksheet.acell('A2').value
            if income_value is not None:
                self.income = float(income_value)
            else:
                self.income = 0

            expenses_records = self.worksheet.get_all_records()
            # Skip the header row and any other non-expense rows
            self.expenses = [record for record in expenses_records if record.get('description')]
            print("Welcome to your Personal Budget Plan")
        except (gspread.exceptions.APIError, ValueError) as e:
            print(f"Clear Income of: {e}")

    def load_data_from_file(self, filename):
        """
        This method is useful for initializing a FinancialTracker instance with previously saved financial data from a file, 
        allowing the program to continue working with previously entered income and expense data. 
        The exception handling ensures that the program does not crash if the specified file is missing.
        """
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                self.income = data["income"]
                self.expenses = data["expenses"]
            print(f"Data loaded from {filename}")
        except FileNotFoundError:
            print(f"No data found in {filename}.")

            # Create the file with default data if it does not exist, error solve using hosted ChatGPT.
            self.save_data_to_file(filename)
        except json.JSONDecodeError:
            print(f"File {filename} contains invalid JSON. Initializing with default values.")
            self.save_data_to_file(filename)

    def set_income(self, amount):
        """
        The process determines whether the amount passed is less than zero.
        A ValueError with the message "Income cannot be less than 0" is raised if the amount is negative. 
        This guarantees that there is no way to set the revenue to a negative amount.
        """
        try:
            if amount < 0:
                raise ValueError("Income cannot be negative.")
            self.income = amount
            self.worksheet.update(range_name='A2', values=[[self.income]])
        except gspread.exceptions.APIError as e:
            print(f"Error updating Google Sheet: {e}")
        except ValueError as ve:
            print(ve)

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
        return self.income - self.total_expenses()
    
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
    
    def save_data_to_file(self, filename):
        """
        This approach is handy for saving financial data to a file in JSON format, which can then be loaded back into the program as needed.
        The exception handling ensures that all potential file operation problems are handled gracefully and reported.
        """
        with open(filename, 'w') as file:
            json.dump({"income": self.income, "expenses": self.expenses}, file)
        print(f"Data saved to {filename}")

def main():
    """
    This will contain the primary logic of the financial tracker.
    """
    sheet = SHEET
    tracker = FinancialTracker(sheet)

    # This line calls the load_data_from_file method of the tracker object to load any existing budget data from a file named Personal Financial Plan
    tracker.load_data_from_file("Personal_Financial_Plan.json")

    # Set the monthly income
    while True:
        try:
            income = float(input("\nEnter your total monthly income: £\n"))
            tracker.set_income(income)
            break
        except ValueError as e:
            print(e)
    
    # Add expenses
    while True:
        description = input("\nEnter expense description (or 'done' to finish): \n")
        if description.lower() == 'done':
            break
        category = input("\nEnter expense category: \n")
        while True:
            try:
                amount = float(input(f"\nEnter amount for {description}: £\n"))
                tracker.add_expense(description, amount, category)
                break
            except ValueError:
                print("Please enter a valid number.")

    # Display the budget summary
    tracker.display_summary()

    # Save data to a file
    tracker.save_data_to_file("Personal_Financial_Plan.json")

if __name__ == "__main__":
    main()