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

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('Personal_Financial_Plan')

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
        self.load_data_from_worksheet()


