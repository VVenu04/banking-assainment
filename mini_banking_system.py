
import os
from datetime import datetime

USERS_FILE = "users.txt"
ACCOUNTS_FILE = "accounts.txt"
TRANSACTIONS_FILE = "transactions.txt"

def read_users():#read users from users file
    users = {}                                                                  
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r") as file:
                for line in file:
                    user_Nic, password = line.strip().split(',')
                    users[user_Nic] = password
        except ValueError:
            print("password or id wrong")
    return users

def generate_account_number():#create account number
    acnumbers = set()
    if os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, "r") as file:
            for line in file:
                acc = line.strip().split(',')[0]
                acnumbers.add(acc)
    while True:
        acc_no = str(datetime.now().strftime("%H%M%S"))
        if acc_no not in acnumbers:
            return acc_no

def create_customer_login():
    user_Nic = input("Enter new customer nic number(user id): ")
    password = input("Enter password: ")
    full_name = input("Enter full name: ")
    with open(USERS_FILE, "a") as file:
        file.write(f"{full_name:20},{user_Nic:10},{password:10}\n")
    print("Customer login created.")

    
    while True:
        try:
            balance = float(input("enter initial balance (must be > 0): "))
            if balance <= 0:
                print("initial balance must be greater than 0.")
                continue
            break
        except ValueError:
            print("invalid amount. Please enter a number.")

    acc_no = generate_account_number()
    with open(ACCOUNTS_FILE, "a") as file:
        file.write(f"{acc_no},{user_Nic},{full_name},{balance}\n")
    transaction(user_Nic, "Account Created", balance, balance)
    print("Account created. Your Account Number is : ",acc_no)

def find_account(user_Nic):
    if os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, "r") as file:
            for line in file:
                acc_no, user, name, balance = line.strip().split(',')
                if user == user_Nic:
                    return acc_no, user, name, float(balance)
    return None

def update_balance(account_number, new_balance):
    lines = []
    with open(ACCOUNTS_FILE, "r") as file:
        lines = file.readlines()
    with open(ACCOUNTS_FILE, "w") as file:
        for line in lines:
            acc_no, user, name, balance = line.strip().split(',')
            if acc_no == account_number:
                file.write(f"{acc_no},{user},{name},{new_balance}\n")
            else:
                file.write(line)

def transaction(user_Nic, trans_type, amount, balance):
    t = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(TRANSACTIONS_FILE, "a") as file:
        file.write(f"{t},{user_Nic},{trans_type},{amount},{balance}\n")

def view_account_by_number():
    acc_no = input("Enter account number: ")
    with open(ACCOUNTS_FILE, "r") as file:
        for line in file:
            acc, user, name, balance = line.strip().split(',')
            if acc == acc_no:
                print(f"\nAccount Number: {acc}")
                print(f"user_Nic: {user}")
                print(f"Name: {name}")
                print(f"Balance: ₹{balance}")
                return
    print("Account not found")

def view_all_transactions():
    if not os.path.exists(TRANSACTIONS_FILE):
        print("No transactions found")
        return
    print(f"\n{'Date & Time':20} | {'User':15} | {'Type':20} | {'Amount':>10} | {'Balance':>10}")
    print("-" * 100)
    with open(TRANSACTIONS_FILE, "r") as file:
        for line in file:
            dt, user, ttype, amount, balance = line.strip().split(',')
            print(f"{dt:20} | {user:15} | {ttype:20} | ₹{amount:>10} | ₹{balance:>10}")

def check_balance(user_Nic):
    acc = find_account(user_Nic)
    if acc:
        acc_no, user, name, balance = acc
        print(f"\nAccount Number: {acc_no}")
        print(f"Name: {name}")
        print(f"Current Balance: ₹{balance}")
    else:
        print("Account not found")

def deposit(user_Nic):
    acc = find_account(user_Nic)
    if acc:
        acc_no, user, name, balance = acc
        while True:
            try:
                amount = float(input("Enter amount to deposit: "))
                if amount <= 0:
                    print("Amount must be greater than 0")
                    continue
                break
            except ValueError:
                print("Invalid input")
        new_balance = balance + amount
        update_balance(acc_no, new_balance)
        transaction(user_Nic, "Deposit", amount, new_balance)
        print("Deposit successful")
    else:
        print("Account not found")

def withdraw(user_Nic):
    acc = find_account(user_Nic)
    if acc:
        acc_no, user, name, balance = acc
        while True:
            try:
                amount = float(input("Enter amount to withdraw: "))
                if amount <= 0:
                    print("Amount must be greater than 0")
                    continue
                if amount > balance:
                    print("Insufficient balance")
                    return
                break
            except ValueError:
                print("Invalid input.")
        new_balance = balance - amount
        update_balance(acc_no, new_balance)
        transaction(user_Nic, "Withdraw", -amount, new_balance)
        print("Withdrawal successful")
    else:
        print("Account not found")

def view_my_transactions(user_Nic):
    print(f"\n{'Date & Time':20} | {'Type':20} | {'Amount':>15} | {'Balance':>15}")
    print("-" * 100)
    with open(TRANSACTIONS_FILE, "r") as file:
        for line in file:
            dt, user, ttype, amount, balance = line.strip().split(',')
            if user == user_Nic:
                print(f"{dt:20} | {ttype:20} | ₹{amount:>15} | ₹{balance:>15}")

def admin_menu():
    while True:
        print("\n============ Admin Menu ===============")
        print("1. Create Customer Login & Account")
        print("2. View Account by Number")
        print("3. View All Transactions")
        print("4. Deposit to Account")
        print("5. Withdraw from Account")
        print("6. Check Balance")
        print("7. Logout")
        choice = input("Choose your option: ")

        if choice == "1":
            create_customer_login()
        elif choice == "2":
            view_account_by_number()
        elif choice == "3":
            view_all_transactions()
        elif choice == "4":
            deposit(input("Enter customer user nic number to deposit money: "))
        elif choice == "5":
            withdraw(input("Enter customer user nic number to withdraw money: "))
        elif choice == "6":
            check_balance(input("Enter customer user nic number to check balance: "))
        elif choice == "7":
            break
        else:
            print("Invalid option")

def customer_menu(user_Nic):
    while True:
        print("\n========== Customer Menu ===========")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. View My Transactions")
        print("4. Check Balance")
        print("5. Logout")
        choice = input("Choose your option: ")

        if choice == "1":
            deposit(user_Nic)
        elif choice == "2":
            withdraw(user_Nic)
        elif choice == "3":
            view_my_transactions(user_Nic)
        elif choice == "4":
            check_balance(user_Nic)
        elif choice == "5":
            break
        else:
            print("Invalid option")

def login():
    print("\n============== Login ====================")
    user_Nic = input("Enter ID: ")
    password = input("Enter Password: ")

    if user_Nic == "admin" and password == "1234":#admin id ,password
        print("Welcome Admin")
        admin_menu()
    else:
        users = read_users()
        if user_Nic in users and users[user_Nic] == password:
            print(f"Welcome {user_Nic}!")
            customer_menu(user_Nic)
        else:
            print("Invalid login")

def main():
    while True:
        print("\n=========== Mini Banking System =============")
        print("1. Login")
        print("2. Exit")
        choice = input("Choose your option: ")
        if choice == "1":
            login()
        elif choice == "2":
            print("Goodbye")
            break
        else:
            print("Invalid option")

main()
