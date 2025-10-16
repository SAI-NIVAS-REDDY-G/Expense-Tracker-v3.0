# -----------------------------------------------
# Expense Tracker v3.0
# -----------------------------------------------

import csv
from datetime import datetime, timedelta
import os
from tabulate import tabulate
from colorama import Fore, Style
import matplotlib.pyplot as plt

FILE_NAME = "expenses.csv"

# ------------------------------------------------
# Ensure CSV file exists
# ------------------------------------------------
if not os.path.exists(FILE_NAME):
    with open(FILE_NAME, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Category", "Description", "Amount"])

# ------------------------------------------------
# Add Expense
# ------------------------------------------------
def add_expense():
    date = datetime.now().strftime("%Y-%m-%d")
    category = input("Enter category (Food, Travel, Shopping, etc.): ").strip().title()
    description = input("Enter description: ").strip()

    while True:
        try:
            amount = float(input("Enter amount: "))
            break
        except ValueError:
            print(Fore.RED + "Invalid amount! Enter a number." + Style.RESET_ALL)

    with open(FILE_NAME, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([date, category, description, amount])

    print(Fore.GREEN + f"\n✅ Expense added: {category} - ₹{amount:.2f} on {date}" + Style.RESET_ALL)

# ------------------------------------------------
# Read Expenses
# ------------------------------------------------
def read_expenses():
    with open(FILE_NAME, "r") as file:
        reader = csv.reader(file)
        next(reader)
        return list(reader)

# ------------------------------------------------
# View Expenses
# ------------------------------------------------
def view_expenses(expenses=None):
    if expenses is None:
        expenses = read_expenses()
    if not expenses:
        print(Fore.YELLOW + "\nNo expenses found!" + Style.RESET_ALL)
        return

    table = []
    total = 0
    for row in expenses:
        date, category, description, amount = row
        total += float(amount)
        table.append([date, category, description, f"₹{float(amount):.2f}"])

    print("\n" + tabulate(table, headers=["Date", "Category", "Description", "Amount"], tablefmt="grid"))
    print(Fore.CYAN + f"\nTotal Spending: ₹{total:.2f}" + Style.RESET_ALL)

# ------------------------------------------------
# Filter by Category
# ------------------------------------------------
def filter_by_category():
    category = input("Enter category to filter: ").strip().title()
    expenses = [row for row in read_expenses() if row[1] == category]
    if not expenses:
        print(Fore.YELLOW + f"\nNo expenses found for '{category}'!" + Style.RESET_ALL)
        return
    view_expenses(expenses)

# ------------------------------------------------
# Filter by Date / Range
# ------------------------------------------------
def filter_by_date():
    print("\nFilter Options:")
    print("1. Specific Date (YYYY-MM-DD)")
    print("2. Last 7 Days")
    print("3. Current Month")
    print("4. Custom Range")
    choice = input("Choose option (1-4): ").strip()

    expenses = read_expenses()
    filtered = []

    if choice == "1":
        date_input = input("Enter date (YYYY-MM-DD): ").strip()
        filtered = [row for row in expenses if row[0] == date_input]

    elif choice == "2":
        today = datetime.now().date()
        last_week = today - timedelta(days=7)
        filtered = [row for row in expenses if last_week <= datetime.strptime(row[0], "%Y-%m-%d").date() <= today]

    elif choice == "3":
        today = datetime.now()
        filtered = [row for row in expenses if datetime.strptime(row[0], "%Y-%m-%d").month == today.month and
                    datetime.strptime(row[0], "%Y-%m-%d").year == today.year]

    elif choice == "4":
        start_date = input("Enter start date (YYYY-MM-DD): ").strip()
        end_date = input("Enter end date (YYYY-MM-DD): ").strip()
        start_dt = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_dt = datetime.strptime(end_date, "%Y-%m-%d").date()
        filtered = [row for row in expenses if start_dt <= datetime.strptime(row[0], "%Y-%m-%d").date() <= end_dt]

    else:
        print(Fore.RED + "Invalid choice!" + Style.RESET_ALL)
        return

    if not filtered:
        print(Fore.YELLOW + "\nNo expenses found for this period!" + Style.RESET_ALL)
        return

    view_expenses(filtered)

# ------------------------------------------------
# Show Total Spending
# ------------------------------------------------
def show_total_spending():
    expenses = read_expenses()
    if not expenses:
        print(Fore.YELLOW + "\nNo expenses found!" + Style.RESET_ALL)
        return
    total = sum(float(row[3]) for row in expenses)
    print(Fore.CYAN + f"\n💰 Total Spending: ₹{total:.2f}" + Style.RESET_ALL)

# ------------------------------------------------
# Visualizations
# ------------------------------------------------
def visualize_spending():
    expenses = read_expenses()
    if not expenses:
        print(Fore.YELLOW + "\nNo expenses found!" + Style.RESET_ALL)
        return

    print("\nVisualization Options:")
    print("1. Category-wise Spending (Pie Chart)")
    print("2. Monthly Spending Trend (Bar Chart)")
    print("3. Weekly/Daily Trend (Last 7 Days)")
    choice = input("Choose option (1-3): ").strip()

    if choice == "1":
        category_totals = {}
        for _, category, _, amount in expenses:
            category_totals[category] = category_totals.get(category, 0) + float(amount)
        plt.figure(figsize=(7,7))
        plt.pie(category_totals.values(), labels=category_totals.keys(), autopct='%1.1f%%', startangle=140)
        plt.title("Category-wise Spending")
        plt.show()

    elif choice == "2":
        monthly_totals = {}
        for date, _, _, amount in expenses:
            month = datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m")
            monthly_totals[month] = monthly_totals.get(month, 0) + float(amount)
        months = list(monthly_totals.keys())
        totals = list(monthly_totals.values())
        plt.figure(figsize=(10,5))
        plt.bar(months, totals, color='skyblue')
        plt.xlabel("Month")
        plt.ylabel("Total Spending (₹)")
        plt.title("Monthly Spending Trend")
        plt.show()

    elif choice == "3":
        today = datetime.now().date()
        last_week = [today - timedelta(days=i) for i in range(6, -1, -1)]
        daily_totals = {day.strftime("%Y-%m-%d"): 0 for day in last_week}
        for date, _, _, amount in expenses:
            if date in daily_totals:
                daily_totals[date] += float(amount)
        plt.figure(figsize=(10,5))
        plt.plot(list(daily_totals.keys()), list(daily_totals.values()), marker='o', color='orange')
        plt.xlabel("Date")
        plt.ylabel("Spending (₹)")
        plt.title("Daily Spending - Last 7 Days")
        plt.grid(True)
        plt.show()

    else:
        print(Fore.RED + "Invalid option!" + Style.RESET_ALL)

# ------------------------------------------------
# Menu Function
# ------------------------------------------------
def show_menu():
    print("\n===== EXPENSE TRACKER v3.0 =====")
    print("1. Add Expense")
    print("2. View All Expenses")
    print("3. Filter by Category")
    print("4. Filter by Date / Range")
    print("5. Show Total Spending")
    print("6. Visualize Spending")
    print("7. Exit")

# ------------------------------------------------
# Main Loop
# ------------------------------------------------
while True:
    show_menu()
    choice = input("Enter your choice (1-7): ").strip()

    if choice == "1":
        add_expense()
    elif choice == "2":
        view_expenses()
    elif choice == "3":
        filter_by_category()
    elif choice == "4":
        filter_by_date()
    elif choice == "5":
        show_total_spending()
    elif choice == "6":
        visualize_spending()
    elif choice == "7":
        print(Fore.GREEN + "\nGoodbye! 👋" + Style.RESET_ALL)
        break
    else:
        print(Fore.RED + "\nInvalid choice! Please try again." + Style.RESET_ALL)