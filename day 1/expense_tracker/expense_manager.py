import json

FILE_PATH = "expense_tracker/data/expenses.json"

def load_expenses():
    try:
        with open(FILE_PATH, "r") as file:
            return json.load(file)
    except:
        return []

def save_expenses(expenses):
    with open(FILE_PATH, "w") as file:
        json.dump(expenses, file, indent=4)

def add_expense():
    name = input("Expense Name: ")
    amount = float(input("Amount: "))

    expense = {
        "name": name,
        "amount": amount
    }

    expenses = load_expenses()
    expenses.append(expense)

    save_expenses(expenses)

    print("Expense Added")

def view_expenses():
    expenses = load_expenses()

    if not expenses:
        print("No expenses found")
        return

    for expense in expenses:
        print(expense)