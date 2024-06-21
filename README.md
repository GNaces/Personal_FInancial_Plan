# Personal Financial Plan

Personal Financial Plan is a Python terminal application that runs on the Code Institute mock terminal on Heroku.

It is an organized strategy to manage your funds on a monthly basis. Individuals who consistently adhere to a personal monthly financial plan can gain control of their finances, achieve their financial goals, and strive toward long-term financial security and independence.

Here is the live version of my project.

![screen_responsive](assets/Responsive.png)

## Conception

- My initial step was to draw a flow diagram of my scope for the Personal Financial Plan concept.

- The Personal Financial Plan lets users keep track of their monthly income and expenses. It allows you to imput revenue, add expenses with description and categories, view a budget summary, and store the data to a file for reference.

![flow_chart](assets/Flow%20chart.png)

## Setup of Gitpod Workspace and resources

I made use of Code Institutes "Love Sandwiches Walkthrough Project", "Getting Set Up" course videos for the following:
 - [Creating a Google Sheet](https://youtu.be/4MWpwuPpSCA).
 - [To activate API credentials](https://youtu.be/WTll5p4N7hE).
 - [Setup of Gitpod Workspace](https://youtu.be/3ikrLWM0QqU).
 - [Connecting to the API with Python](https://youtu.be/lPTKUiafTRY).

## Features

### Existing Features

- When initializing the program, the user is dispalyed a welcome message.

![welcome](assets/Home.png)

- Set Income - allows user to input monthly income, enabling proper financial tracking and budget management. Users enter their income amount.

![enter_income](assets/Enter%20Income.png)

- Entered income amount will automatically appear and saved in the Personal Financial Plan Google worksheet.

![income_saved](assets/Worksheet%20Income%20updated.png)

- Whenever a negative income amount is entered, the user will be promted that "Income cannot be negative"

![income_negative](assets/Income%20cannot%20be%20negative.png)

- Add Expense Description - allows user to describe expenses in details.

![enter_description](assets/Expense%20description.png)

- Add Category - enable user to categorize expenses based on the nature of usage.

![enter_category](assets/Expense%20Category.png)

- Add Amount - user will define how much is spent on this category for the month.

![enter_amount](assets/Expense%20Amount.png)

- Whenever a negative expense amount is entered, the user will be promted that "Expenses cannot be negative"

![expenses_negative](assets/Expense%20cannot%20be%20negative.png)

- After the user is satisfied entering all the expenses needed to be considered, user will enter 'done' to finish the process. Then a summary of Monthly Personal Finances will be printed in the screen.

![done_print_summary](assets/done%20and%20print%20summary.png)

- When all data is entered, subsequently all data entered will be saved in the Personal Financial Plan Google Spreadsheet.

![all_saved](assets/Update%20google%20worksheet.png)

### Future Features

- Expand the code and incorporate the budgeted monthly income and expenses versus the actual monthly income and expenses.
- Allow historical data to be retrived and new data stored for further future references.


## Testing

- 