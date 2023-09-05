#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import json
import csv
from datetime import datetime
from tabulate import tabulate
import getpass
t_expense = 0
t_income = 0
t_savings = 0
perc_savings = 0

# Initialize a dictionary to store user data
users_data = {}

def load_data():
    try:
        with open('users_data.json', 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {
            "demo_account": {
                "name": "Demo User",
                "password": "Hello@123",
                "expenses": [],
                "incomes": []
            }
        }

def save_data(data):
    with open('users_data.json', 'w') as file:
        json.dump(data, file, indent=4)

def login():
    username = input("Username: ").strip().lower()  # Convert to lowercase and remove whitespace
    password = getpass.getpass("Password: ")  # Use getpass to securely input the password

    if username in users_data and users_data[username]['password'] == password:
        return username
    else:
        print("Invalid username or password.")
        return None

def add_expense(user):
    purpose = input("Enter the purpose of the expense: ")
    amount = float(input("Enter the amount: "))
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    users_data[user]['expenses'].append({'purpose': purpose, 'amount': amount, 'date': date})
    save_data(users_data)
    print("Expense added successfully.")

def add_income(user):
    amount = float(input("Enter the amount of income: "))
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    users_data[user]['incomes'].append({'amount': amount, 'date': date})
    save_data(users_data)
    print("Income added successfully.")

# Function to display current balance
def display_balance(user):
    total_income = sum(item['amount'] for item in users_data[user]['incomes'])
    total_expenses = sum(item['amount'] for item in users_data[user]['expenses'])
    current_balance = total_income - total_expenses
    return current_balance

# Function to display total expenses
def display_total_expenses(user):
    expenses = users_data[user]['expenses']
    total_expenses = calculate_total_expenses(expenses)
    
    if expenses:
        expense_table = []
        for expense in expenses:
            expense_table.append([expense['date'], expense['purpose'], expense['amount']])
        
        print("\033[94mExpense Details:\033[0m")
        print(tabulate(expense_table, headers=["Date", "Purpose", "Amount"], tablefmt="fancy_grid"))
    
    print("\033[91mTotal Expenses:\033[0m", total_expenses)
    return total_expenses

# Function to calculate total expenses
def calculate_total_expenses(expenses):
    return sum(expense['amount'] for expense in expenses)

# Function to calculate statistics
def calculate_statistics(expenses, incomes):
    total_expenses = sum(item['amount'] for item in expenses)
    total_income = sum(item['amount'] for item in incomes)
    savings = total_income - total_expenses
    if total_income > 0:
        savings_percentage = (savings / total_income) * 100
    else:
        savings_percentage = 0
    statistics = [
        ["Total Expenses", total_expenses],
        ["Total Income", total_income],
        ["Savings", savings],
        ["Savings Percentage", f"{savings_percentage:.2f}%"]
    ]
    
    statistics_table = tabulate(statistics, headers=["Metric", "Value"], tablefmt="fancy_grid")
    
    return total_expenses, total_income, savings, savings_percentage, statistics_table

def export_to_csv(user):
    filename = f'{user}_expenses.csv'
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Purpose", "Amount"])

        for expense in users_data[user]['expenses']:
            writer.writerow([expense['date'], expense['purpose'], expense['amount']])
        writer.writerow([])  # Empty row as spacing

        writer.writerow(["Income Date", "Income Amount"])
        for income in users_data[user]['incomes']:
            writer.writerow([income['date'], income['amount']])
        writer.writerow([])  # Empty row as spacing
        writer.writerow(["Statistics"])
        writer.writerow(["Total Expenses", "Total Income", "Savings", "Savings Percentage"])
        writer.writerow([t_expense, t_income, t_savings, f"{perc_savings:.2f}%"])

    print(f"Data exported to {filename}")
# Main Function
if __name__ == '__main__':
    users_data = load_data()
    print("\033[95mWelcome to Personal Budget Tracker\033[0m")
    try:
        while True:
            print("\033[96m1. Register as a new user")
            print("2. Login to your account")  # Add an option for user registration
            print("3. Exit\033[0m")
            choice = input("\033[94mEnter your choice:\033[0m ")

            if choice == '2':
                user = login()
                if user:
                    user_name = users_data[user]['name']
                    while True:
                        print(f"\033[96m\nWelcome, {user_name}!")
                        print("1. Add Expense")
                        print("2. Add Income")
                        print("3. Calculate Statistics")
                        print("4. Export Expenses to CSV")
                        print("5. Display Current Balance")
                        print("6. Display Total Expenses")
                        print("7. Logout\033[0m")
                        sub_choice = input("\033[94mEnter your choice:\033[0m ")

                        if sub_choice == '1':
                            add_expense(user)
                        elif sub_choice == '2':
                            add_income(user)
                        elif sub_choice == '3':
                            total_expenses, total_income, savings, savings_percentage, statistics_table = calculate_statistics(users_data[user]['expenses'], users_data[user]['incomes'])
                            print("\033[94mSummary:\033[0m")
                            print(statistics_table)
                        elif sub_choice == '4':
                            export_to_csv(user)
                        elif sub_choice == '5':
                            balance = display_balance(user)
                            print("\033[92mCurrent Balance:\033[0m", balance)
                        elif sub_choice == '6':
                            total_expenses = display_total_expenses(user)
                            print("\033[91mTotal Expenses:\033[0m", total_expenses)
                        elif sub_choice == '7':
                            break
                        else:
                            print("\033[91mInvalid choice.\033[0m")
            elif choice == '1':
                register_username = input("Enter a username: ").strip().lower()
                if register_username in users_data:
                    print("Username already exists. Please choose a different username.")
                else:
                    register_name = input("Enter your name: ")
                    register_password = getpass.getpass("Enter a password: ")
                    users_data[register_username] = {
                        "name": register_name,
                        "password": register_password,
                        "expenses": [],
                        "incomes": []
                    }
                    save_data(users_data)
                    print("Registration successful. You can now log in with your new account.")
            elif choice == '3':
                break
            else:
                print("\033[91mInvalid choice.\033[0m")
    except KeyboardInterrupt:
        confirm = input("\nAre you sure you want to quit? (yes/no): ")
        if confirm.lower() == "yes":
            print("\033[93mThank you for using Personal Budget Tracker by Team LinuxNinjas.\033[0m")
        else:
            print("\033[92mResuming Personal Budget Tracker.\033[0m")


# In[ ]:




