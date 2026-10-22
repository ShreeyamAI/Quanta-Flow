import os
import pyfiglet
from termcolor import colored
import pandas as pd
import matplotlib.pyplot as plt
###
###
###
###
###
###
###
###
###
###
###
###
### Name
font = pyfiglet.Figlet(font='cyberlarge')
text = font.renderText("QuantaFlow")

colors = ['magenta', 'red', 'yellow']
split_text = text.split('\n')
colored_text = ''

for line in split_text:
    if line.strip():  
        colored_text += colored(line, colors[split_text.index(line) % len(colors)]) + '\n'

print(colored_text)
print("\033[91mby IRISFinance.IRIS.corp.pvt.ltdred\033[0m")
###
###
###
###Paths
relative_path = "Credentials/credentials.txt"
finance_directory = "FinanceFiles" 
###
###
###
###absolute path
def get_absolute_path(relative_path):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)
###
###
###
###
###
###
###
###
###
###
###
###
###Register user
def register_user(credentials_file):
    while True:
        username = input("Enter your new username: ")
        password = input("Enter your new password: ")
        
        if username == "" or password == "":
            print("Username and password cannot be empty.")
            continue

        if os.path.exists(credentials_file):
            with open(credentials_file, "r") as file:
                for line in file:
                    stored_username, _ = line.strip().split(":")
                    if username == stored_username:
                        print("Username already exists. Please choose a different username.")
                        break
                else:
                    with open(credentials_file, "a") as file:
                        file.write(f"{username}:{password}\n")
                    print("User registered successfully!")
                    return
        else:
            with open(credentials_file, "w") as file:
                file.write(f"{username}:{password}\n")
            print("User registered successfully!")
            return
###
###
###
###
###
###
###
###
###
###
###
###
###Login user
def login_user(credentials_file):
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    
    if username == "" or password == "":
        print("Username and password cannot be empty.")
        return None

    if os.path.exists(credentials_file):
        with open(credentials_file, "r") as file:
            for line in file:
                stored_username, stored_password = line.strip().split(":")
                if username == stored_username and password == stored_password:
                    print("Login successful!")
                    return username
    else:
        print("Credentials file does not exist.")
    
    print("Invalid username or password.")
    return None
###
###
###
###
###
###
###
###
###
###
###
###
###Manage Finance
def manage_finance(username):

    finance_file = os.path.join(get_absolute_path(finance_directory), f'{username}_finance.csv')

    while True:
        print("\nManage Finance Menu:")
        print("1. Add New Expense")
        print("2. View Expenses")
        print("3. View Expenses by Category")
        print("4. Filter Expenses by Date")
        print("5. Monthly Summary")
        print("6. Yearly Summary")
        print("7. Delete Expense")
        print("8. Return to Main Menu")
        
        choice = input("Enter your choice (1-8): ")
        
        if choice == "1":
            add_expense(finance_file)
        elif choice == "2":
            view_expenses(finance_file)
        elif choice == "3":
            view_expenses_by_category(finance_file)
        elif choice == "4":
            filter_expenses_by_date(finance_file)
        elif choice == "5":
            monthly_summary(finance_file)
        elif choice == "6":
            yearly_summary(finance_file)
        elif choice == "7":
            delete_expense(finance_file)
        elif choice == "8":
            print("Returning to Main Menu...")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 8.")
###
###
###
###
###
###
###
###
###
###
###
###
### add exp() 
def add_expense(finance_file):
    if not os.path.exists(finance_file):
        df = pd.DataFrame(columns=['Category', 'Amount', 'Date'])
        df.to_csv(finance_file, index=False)
    else:
        df = pd.read_csv(finance_file)

    category = input("Enter the expense category: ")
    amount = input("Enter the expense amount: ")
    date = input("Enter the date of the expense (YYYY-MM-DD): ")

    try:
        amount = float(amount)
    except ValueError:
        print("Invalid amount. Please enter a numeric value.")
        return

    new_expense_df = pd.DataFrame([{
        'Category': category,
        'Amount': amount,
        'Date': date
    }])

    df = pd.concat([df, new_expense_df], ignore_index=True)
    df.to_csv(finance_file, index=False)

    print("Expense added successfully!")

def view_expenses(finance_file):
    if not os.path.exists(finance_file):
        print("No expenses found.")
        return
    
    df = pd.read_csv(finance_file)
    if df.empty:
        print("No expenses found.")
    else:
        print("\nYour Expenses:")
        print(df.to_string(index=False))

def delete_expense(finance_file):
    if not os.path.exists(finance_file):
        print("No expenses found.")
        return
    
    df = pd.read_csv(finance_file)
    if df.empty:
        print("No expenses found.")
        return
    
    print("\nYour Expenses:")
    print(df.to_string(index=False))
    
    try:
        expense_index = int(input("Enter the index of the expense to delete: "))
        if 0 <= expense_index < len(df):
            df = df.drop(expense_index).reset_index(drop=True)
            df.to_csv(finance_file, index=False)
            print("Expense deleted successfully!")
        else:
            print("Invalid index.")
    except ValueError:
        print("Invalid input. Please enter a valid number.")
###
###
###
###
###
###
###
###
###
###
###
###
### view exp()
def view_expenses_by_category(finance_file):
    if not os.path.exists(finance_file):
        print("No expenses found.")
        return

    df = pd.read_csv(finance_file)
    if df.empty:
        print("No expenses found.")
        return

    category_data = df.groupby('Category')['Amount'].sum()
    
    print("\nExpenses by Category:")
    print(category_data.to_string())
###
###
###
###
###
###
###
###
###
###
###
###
### filter exp()
def filter_expenses_by_date(finance_file):
    if not os.path.exists(finance_file):
        print("No expenses found.")
        return
    
    df = pd.read_csv(finance_file)
    if df.empty:
        print("No expenses found.")
        return

    df['Date'] = pd.to_datetime(df['Date'])

    start_date = input("Enter the start date (YYYY-MM-DD): ")
    end_date = input("Enter the end date (YYYY-MM-DD): ")
    
    try:
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return

    filtered_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

    if filtered_df.empty:
        print("No expenses found in this date range.")
        return

    print("\nFiltered Expenses:")
    print(filtered_df.to_string(index=False))
###
###
###
###
###
###
###
###
###
###
###
###
### month sum()
def monthly_summary(finance_file):
    if not os.path.exists(finance_file):
        print("No expenses found.")
        return
    
    df = pd.read_csv(finance_file)
    if df.empty:
        print("No expenses found.")
        return

    df['Date'] = pd.to_datetime(df['Date'])

    df.set_index('Date', inplace=True)

    monthly_data = df.resample('M')['Amount'].sum()
    
    print("\nMonthly Expense Summary:")
    print(monthly_data.to_string())
###
###
###
###
###
###
###
###
###
###
###
###
### year sum()
def yearly_summary(finance_file):
    if not os.path.exists(finance_file):
        print("No expenses found.")
        return
    
    df = pd.read_csv(finance_file)
    if df.empty:
        print("No expenses found.")
        return

    df['Date'] = pd.to_datetime(df['Date'])

    df.set_index('Date', inplace=True)

    yearly_data = df.resample('Y')['Amount'].sum()
    
    print("\nYearly Expense Summary:")
    print(yearly_data.to_string())
###
###
###
###
###
###
###
###
###
###
###
###
### finamce_file()
def get_finance_file_path(username):
    base_dir = os.path.normpath(get_absolute_path(finance_directory))

    if not os.path.exists(base_dir):
        print(f"Error: The directory '{base_dir}' does not exist.")
        return None

    finance_file = os.path.join(base_dir, f"{username}_finance.csv")
    
    if not os.path.exists(finance_file):
        print(f"Error: No finance data found for user {username}. Expected file path: {finance_file}")
        return None
    
    return finance_file
###
###
###
###
###
###
###
###
###
###
###
###
### visualize data()
def see_graphical_visualization(username):
    finance_file = get_finance_file_path(username)
    
    if finance_file is None:
        return
    
    df = pd.read_csv(finance_file)

    if df.empty:
        print("No expense data available to visualize.")
        return

    while True:
        print("\nChoose the type of visualization:")
        print("1. Shows my expenses by category.")
        print("2. Displays my expenses over time.")
        print("3. Illustrates the distribution of my expenses by category.")
        print("4. Visualize the distribution of my expenses")
        print("5. Return to Main Menu")
        
        choice = input("Enter your choice (1-5): ")
        
        if choice == "1":
            plot_bar_chart(df)
        elif choice == "2":
            plot_line_chart(df)
        elif choice == "3":
            plot_pie_chart(df)
        elif choice == "4":
            plot_histogram(df)
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

def plot_bar_chart(df):
    category_data = df.groupby('Category')['Amount'].sum()
    
    plt.figure(figsize=(10, 6))
    category_data.plot(kind='bar', color='skyblue')
    plt.title('Expense by Category')
    plt.xlabel('Category')
    plt.ylabel('Total Amount')
    plt.xticks(rotation=45)
    plt.show()

def plot_line_chart(df):
    df['Date'] = pd.to_datetime(df['Date'])
    df.sort_values('Date', inplace=True)
    
    plt.figure(figsize=(10, 6))
    plt.plot(df['Date'], df['Amount'], marker='o', linestyle='-', label='Expenses')
    plt.title('Expenses Over Time')
    plt.xlabel('Date')
    plt.ylabel('Amount')
    plt.xticks(rotation=45)
    plt.legend()
    plt.show()

def plot_pie_chart(df):
    category_data = df.groupby('Category')['Amount'].sum()
    
    plt.figure(figsize=(8, 8))
    category_data.plot(kind='pie', autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
    plt.title('Expense Distribution by Category')
    plt.ylabel('')
    plt.show()

def plot_histogram(df):
    plt.figure(figsize=(10, 6))
    plt.hist(df['Amount'], bins=10, color='lightgreen', edgecolor='black')
    plt.title('Histogram of Expenses')
    plt.xlabel('Expense Amount')
    plt.ylabel('Frequency')
    plt.grid(axis='y')
    plt.show()
###
###
###
###
###
###
###
###
###
###
###
###
### updatepass()
def update_password(credentials_file, username):
    try:
        with open(credentials_file, "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("Credentials file not found.")
        return

    user_found = False
    for i, line in enumerate(lines):
        stored_username, stored_password = line.strip().split(":")
        if username == stored_username:
            user_found = True
            break

    if not user_found:
        print("Username not found.")
        return

    old_password = input("Enter your old password: ")
    if old_password != stored_password:
        print("Old password is incorrect.")
        return

    new_password = input("Enter your new password: ")

    lines[i] = f"{username}:{new_password}\n"

    with open(credentials_file, "w") as file:
        file.writelines(lines)

    print("Password updated successfully!")
###
###
###
###
###
###
###
###
###
###
###
###
### Manageacc()
def manage_account(username):
    while True:
        print("\nManage Account Menu:")
        print("1. Update Password")
        print("2. Return to Main Menu")
        
        choice = input("Enter your choice (1-2): ")
        
        if choice == "1":
            update_password(get_absolute_path(relative_path), username)
        elif choice == "2":
            print("Returning to Main Menu...")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 2.")

###
###
###
###
###
###
###
###
###
###
###
###
### View users()
def view_existing_users(credentials_file):
    print("\nExisting Users:")
    if os.path.exists(credentials_file):
        with open(credentials_file, "r") as file:
            for line in file:
                username, _ = line.strip().split(":")
                print(username)
    else:
        print("No users found.")
###
###
###
###
###
###
###
###
###
###
###
###
### docX()
###
###
###
###
###
###
###
###
###
###
###
###
### MainSC()
def main():
    credentials_file = get_absolute_path(relative_path)
    
    if not os.path.exists(os.path.dirname(credentials_file)):
        print("Error: The directory for credentials does not exist. Please check the path.")
        return
    
    while True:
        print("\nWelcome to the Personal Finance and Budget Tracker!")
        print("1. Register New User")
        print("2. Login")
        print("3. View Existing Users")
        print("4. Exit Program")
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == "1":
            register_user(credentials_file)
        elif choice == "2":
            username = login_user(credentials_file)
            
            if username:
                while True:
                    print("\nMenu:")
                    print("1. Manage Finance")
                    print("2. See visualize my expenses")
                    print("3. Manage Account")
                    print("4. Logout")
                    
                    menu_choice = input("\nEnter your choice (1-4): ")
                    
                    if menu_choice == "1":
                        manage_finance(username)
                    elif menu_choice == "2":
                        see_graphical_visualization(username)
                    elif menu_choice == "3":
                        manage_account(username)
                    elif menu_choice == "4":
                        print("Logging out...")
                        break
                    else:
                        print("Invalid choice. Please enter a number between 1 and 4.")
        elif choice == "3":
            view_existing_users(credentials_file)
        elif choice == "4":
            print("\nThank you for using our service.\nExiting the program...")
            break
        else:
            print("\nInvalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()
