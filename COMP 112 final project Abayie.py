import tkinter as tk
from tkinter import messagebox
import random
import csv
import os
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd

categories = ['Food', 'Clothing', 'Rent', 'Entertainment', 'Miscellaneous']
def write_to_csv(user_data, file='finance_data.csv'):
    """sig: str->str
        writes data to csv file"""
    try:
        with open(file, mode='a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(user_data)
    except Exception as e:
        print(f"Error writing to CSV: {e}")


def generate_fake_data():
    """sig: str->str
        generates the fake data from january to November to be stored in a csv file"""
    months = ["2024-01", "2024-02", "2024-03", "2024-04", "2024-05", "2024-06", "2024-07", "2024-08", "2024-09", "2024-10", "2024-11"]
    fake_data = []

    for month in months:
        income = round(random.uniform(2000, 5000), 2)
        total_budgeted = 0
        total_actual = 0

        for category in categories:
            budgeted = round(random.uniform(100, 1000), 2)
            actual = round(budgeted + random.uniform(-200, 200), 2)
            total_budgeted += budgeted
            total_actual += actual
            fake_data.append([month, income, category, budgeted, actual])

        savings = round(income - total_actual, 2)
        advice = "Great job saving!" if savings > 0 else "Try to save more next month."
        fake_data.append([month, income, "Total", round(total_budgeted, 2), round(total_actual, 2), savings, advice])
    return fake_data


def read_csv(file='finance_data.csv'):
    """sig: str->str
        read data from csv file"""
    data = []
    try:
        with open(file, mode='r') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                data.append(row)
    except FileNotFoundError:
        print("CSV file not found.")
    return data


def collect_data():
    """sig: str->str
        allows user to input income and expenditures and handling errors using try except block"""
    current_month = datetime.now().strftime("%Y-%m")
    try:
        income = round(float(entry_income.get()), 2)
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter a valid number for income.")
        return
    budgeted = {}
    actual_spent = {}
    for category in categories:
        try:
            budgeted_value = entry_budgeted[category].get()
            if not budgeted_value:
                raise ValueError(f"{category} budgeted amount cannot be empty.")
            budgeted[category] = round(float(budgeted_value), 2)
        except ValueError as e:
            messagebox.showerror("Invalid input", f"Please enter a valid number for {category} budgeted amount.\nError: {str(e)}")
            return
        try:
            spent_value = entry_actual_spent[category].get()
            if not spent_value:
                raise ValueError(f"{category} actual spent amount cannot be empty.")
            actual_spent[category] = round(float(spent_value), 2)
        except ValueError as e:
            messagebox.showerror("Invalid input", f"Please enter a valid number for {category} actual spending.\nError: {str(e)}")
            return
    for category in categories:
        user_data = [current_month, income, category, round(budgeted[category], 2), round(actual_spent[category], 2)]
        write_to_csv(user_data)
    total_budgeted = round(sum(budgeted.values()), 2)
    total_actual = round(sum(actual_spent.values()), 2)
    savings = round(income - total_actual, 2)
    advice = "Great job saving!" if savings >= 500 else "Try to save more next month."
    user_data_total = [current_month, income, "Total", total_budgeted, total_actual, savings, advice]
    write_to_csv(user_data_total)
    update_totals(income, total_actual, savings)
    all_data = read_csv()
    total_income_all = 0
    total_expenditure_all = 0
    total_savings_all = 0
    for row in all_data:
        try:
            if len(row) >= 6:
                total_income_all += float(row[1])
                total_expenditure_all += float(row[4])
                total_savings_all += float(row[5])
        except ValueError:
            pass  
    new_user_data = [current_month, income, "Sum of All", total_income_all, total_expenditure_all, total_savings_all, savings]
    write_to_csv(new_user_data)
    messagebox.showinfo("Success", f"Data saved successfully!\nTotal Savings for the month: ${savings:.2f}")


def update_totals(income, expenditure, savings):
    """sig: str->str
        gets total amount of expenditure and savings for the month and displays"""
    total_income.set(f"${income:.2f}")
    total_expenditure.set(f"${expenditure:.2f}")
    total_savings.set(f"${savings:.2f}")
    
    overall_advice = "Great job saving! Keep it up!" if savings > 0 else "Try to save more next time."
    total_advice.set(overall_advice)


def plot_graphs():
    """sig: str->str
        for plotting graph of income, expense and savings against time(month)"""
    data = read_csv()
    months = []
    income = []
    actual_spending = []
    savings = []
    for row in data:
        try:
            if len(row) >= 6:
                month = row[0]
                income_value = round(float(row[1]), 2)
                actual_spending_value = round(float(row[4]), 2)
                savings_value = round(float(row[5]), 2)

                months.append(month)
                income.append(income_value)
                actual_spending.append(actual_spending_value)
                savings.append(savings_value)
        except ValueError:
            continue
    if not months:
        messagebox.showerror("No Data", "No valid data found for plotting. Please enter data first.")
        return

    plt.figure(figsize=(10, 6))
    plt.bar(months, income, label="Income", alpha=0.7, color='blue', width=0.2, align='center')
    plt.bar(months, actual_spending, label="Actual Spending", alpha=0.7, color='red', width=0.2, align='edge')
    plt.plot(months, savings, label="Savings", marker='o', color='green', linestyle='-', linewidth=2)

    plt.xlabel('Month')
    plt.ylabel('Amount ($)')
    plt.title('Financial Overview')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(True)
    plt.show()


def setup_gui():
    """sig: str->str
        set up th Graphical User Interface"""
    global entry_income, entry_budgeted, entry_actual_spent, total_income, total_expenditure, total_savings, total_advice
    window = tk.Tk()
    window.title("Financial Budget Tracker")
    window.configure(bg='#1a3d61')
    tk.Label(window, text="Deborah, Welcome to your financial budget tracker!", font=("Arial", 14), bg='#1a3d61', fg="white").grid(row=0, column=0, columnspan=4, pady=20)
    tk.Label(window, text="Enter your income for the month:", font=("Arial", 12), bg='#1a3d61', fg="white").grid(row=1, column=0, columnspan=2, pady=(20, 10))
    tk.Label(window, text="$", font=("Arial", 12), bg='#1a3d61', fg="white").grid(row=1, column=2, pady=(20, 10), padx=(0, 5))
    entry_income = tk.Entry(window, bg='#000000', fg='white', font=("Arial", 12))
    entry_income.grid(row=1, column=3, columnspan=2, pady=(20, 10))
    entry_budgeted = {}
    entry_actual_spent = {}
    row_offset = 2
    for idx, category in enumerate(categories):
        tk.Label(window, text=f"{category}:", font=("Arial", 12), bg='#1a3d61', fg="white").grid(row=row_offset + idx, column=0, pady=5, sticky="e")
        tk.Label(window, text="$", font=("Arial", 12), bg='#1a3d61', fg="white").grid(row=row_offset + idx, column=1, pady=5)

        entry_budgeted[category] = tk.Entry(window, bg='#000000', fg='white', font=("Arial", 12))
        entry_budgeted[category].grid(row=row_offset + idx, column=2, pady=5)

        tk.Label(window, text=f"Spent on {category}:", font=("Arial", 12), bg='#1a3d61', fg="white").grid(row=row_offset + idx, column=3, pady=5, sticky="e")
        tk.Label(window, text="$", font=("Arial", 12), bg='#1a3d61', fg="white").grid(row=row_offset + idx, column=4, pady=5)

        entry_actual_spent[category] = tk.Entry(window, bg='#000000', fg='white', font=("Arial", 12))
        entry_actual_spent[category].grid(row=row_offset + idx, column=5, pady=5)

    submit_button = tk.Button(window, text="Submit", command=collect_data, font=("Arial", 12, "bold"), bg='#003366', fg="black")
    submit_button.grid(row=row_offset + len(categories) + 1, column=1, columnspan=2, pady=20)

    view_graph_button = tk.Button(window, text="View Graph", command=plot_graphs, font=("Arial", 12, "bold"), bg='#003366', fg="black")
    view_graph_button.grid(row=row_offset + len(categories) + 2, column=1, columnspan=2, pady=10)

    tk.Label(window, text="Income:", font=("Arial", 12), bg='#1a3d61', fg="white").grid(row=row_offset + len(categories) + 3, column=0)
    total_income = tk.StringVar()
    tk.Label(window, textvariable=total_income, font=("Arial", 12), bg='#1a3d61', fg="white").grid(row=row_offset + len(categories) + 3, column=1)

    tk.Label(window, text="Expenditure:", font=("Arial", 12), bg='#1a3d61', fg="white").grid(row=row_offset + len(categories) + 4, column=0)
    total_expenditure = tk.StringVar()
    tk.Label(window, textvariable=total_expenditure, font=("Arial", 12), bg='#1a3d61', fg="white").grid(row=row_offset + len(categories) + 4, column=1)

    tk.Label(window, text="Savings:", font=("Arial", 12), bg='#1a3d61', fg="white").grid(row=row_offset + len(categories) + 5, column=0)
    total_savings = tk.StringVar()
    tk.Label(window, textvariable=total_savings, font=("Arial", 12), bg='#1a3d61', fg="white").grid(row=row_offset + len(categories) + 5, column=1)

    tk.Label(window, text="Financial Advice:", font=("Arial", 12), bg='#1a3d61', fg="white").grid(row=row_offset + len(categories) + 6, column=0)
    total_advice = tk.StringVar()
    tk.Label(window, textvariable=total_advice, font=("Arial", 12), bg='#1a3d61', fg="white").grid(row=row_offset + len(categories) + 6, column=1)

    window.mainloop()

if __name__ == "__main__":
    if not os.path.exists('finance_data.csv'):
        with open('finance_data.csv', mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Month', 'Income', 'Category', 'Budgeted Amount', 'Actual Spending', 'Savings', 'Financial Advice'])  # Header row

    fake_data = generate_fake_data()
    for row in fake_data:
        write_to_csv(row)
    setup_gui()
