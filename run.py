import json

# To access and change data on a spreadsheet, import the gspread library.
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
    Manage tracker logic: set income, add expenses, compute totals, worksheets.
    """
    def __init__(self, worksheet):
        """
        Trigger new instance; requires 'self' and one parameter 'worksheet'.
        """
        self.income = 0
        self.expenses = []
        self.worksheet = worksheet
        self.load_from_sheet()

    def load_from_sheet(self):
        """
        Initializes FinancialTracker with saved data from a Google Sheet.
        Continue work with previously entered income and expense data.
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
            print(f"This is your previous income, {e}")

    def load_data_from_file(self, filename):
        """
        Initializes FinancialTracker with saved financial data from a file,
        allows continued use of previously entered income and expense data,
        ensures program doesn't crash if the specified file is missing.
        """
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                self.income = data["income"]
                self.expenses = data["expenses"]
            print(f"Data loaded from {filename}")
        except FileNotFoundError:
            print(f"No data found in {filename}.")

            self.save_data_to_file(filename)
        except json.JSONDecodeError:
            print(f"File {filename} contains invalid JSON. Initiate default.")
            self.save_data_to_file(filename)

    def set_income(self, amount):
        """
        The process determines whether the amount passed is less than zero.
        Raises "Income cannot be less than 0" for negative amounts.
        Ensures revenue cannot be set to a negative amount.
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
        Provides the description, amount, and category of the item,
        adds expense details to self.worksheet as a new row.
        """
        if amount < 0:
            raise ValueError("Expense cannot be negative.")
        self.expenses.append({"description": description, "amount": amount, "category": category})
        self.worksheet.append_row(['', description, amount, category])

    def total_expenses(self):
        """
        Computes total expenses by summing all amounts in the list.
        """
        return sum(expense["amount"] for expense in self.expenses)

    def calculate_remaining_balance(self):
        """
        Calculates remaining balance as income minus total expenses.
        """
        return self.income - self.total_expenses()

    def display_summary(self):
        """
        Includes total earnings and a list of expenses
        with type, amount, and description.
        Total cost subtracted from revenue yields remaining amount.
        """
        print("\n---- Monthly Personal Finances Summary ----")
        print(f"Total Income: £{self.income:.2f}")
        print("Expenses:")
        for expense in self.expenses:
            print(f" - {expense['description']} ({expense['category']}): £{expense['amount']:.2f}")
        print(f"Total Expenses: £{self.total_expenses():.2f}")
        print(f"Remaining Balance: £{self.calculate_remaining_balance():.2f}")

    def save_data_to_file(self, filename):
        """
        Saves financial data to JSON file for future program loading.
        Handles file operation issues gracefully with exception handling.
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

    # This line calls the load_data_from_file method of the tracker object
    # to load any existing budget data from a file named
    # Personal Financial Plan
    tracker.load_data_from_file("Personal_Financial_Plan")

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
                print("Expenses cannot be negative.")

    # Display the budget summary
    tracker.display_summary()

    # Save data to a file
    tracker.save_data_to_file("Personal_Financial_Plan")


if __name__ == "__main__":
    main()
