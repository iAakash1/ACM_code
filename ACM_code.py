import csv
import os
from cryptography.fernet import Fernet
from getpass import getpass

# Generate a key and save it to a file if it doesn't exist
KEY_FILE = 'key.key'
DATA_FILE = 'passwords.csv'

def load_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, 'wb') as key_file:
            key_file.write(key)
    else:
        with open(KEY_FILE, 'rb') as key_file:
            key = key_file.read()
    return Fernet(key)

# Initialize encryption object
cipher = load_key()

# Authenticate the user with a master password
MASTER_PASSWORD = 'admin'  # Change this in a real application
def authenticate():
    password = getpass("Enter the master password: ")
    return password == MASTER_PASSWORD

# Add a new password entry
def add_password():
    if not authenticate():
        print("Authentication failed!")
        return

    account = input("Enter account name: ")
    username = input("Enter username: ")
    password = getpass("Enter password: ")
    encrypted_password = cipher.encrypt(password.encode()).decode()

    with open(DATA_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([account, username, encrypted_password])
    print("Password added successfully.")

# View saved passwords
def view_passwords():
    if not authenticate():
        print("Authentication failed!")
        return

    if not os.path.exists(DATA_FILE):
        print("No passwords saved.")
        return

    with open(DATA_FILE, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            account, username, encrypted_password = row
            print(f"Account: {account}, Username: {username}")

    reveal = input("Do you want to reveal a password? (y/n): ")
    if reveal.lower() == 'y':
        account_to_reveal = input("Enter the account name to reveal the password: ")
        reveal_password(account_to_reveal)

# Reveal a specific password
def reveal_password(account_name):
    if not authenticate():
        print("Authentication failed!")
        return

    with open(DATA_FILE, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            account, username, encrypted_password = row
            if account == account_name:
                decrypted_password = cipher.decrypt(encrypted_password.encode()).decode()
                print(f"Password for {account}: {decrypted_password}")
                return
    print("Account not found.")

# Delete a password entry
def delete_password():
    if not authenticate():
        print("Authentication failed!")
        return

    account_to_delete = input("Enter the account name to delete: ")

    if not os.path.exists(DATA_FILE):
        print("No passwords saved.")
        return

    rows = []
    found = False
    with open(DATA_FILE, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] != account_to_delete:
                rows.append(row)
            else:
                found = True

    if not found:
        print("Account not found.")
        return

    with open(DATA_FILE, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)
    print("Password deleted successfully.")

# Update a password
def update_password():
    if not authenticate():
        print("Authentication failed!")
        return

    account_to_update = input("Enter the account name to update: ")

    if not os.path.exists(DATA_FILE):
        print("No passwords saved.")
        return

    rows = []
    found = False
    with open(DATA_FILE, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == account_to_update:
                found = True
                username = row[1]
                new_password = getpass("Enter the new password: ")
                encrypted_password = cipher.encrypt(new_password.encode()).decode()
                rows.append([account_to_update, username, encrypted_password])
            else:
                rows.append(row)

    if not found:
        print("Account not found.")
        return

    with open(DATA_FILE, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)
    print("Password updated successfully.")

# Main loop
def main():
    while True:
        print("\nPassword Manager")
        print("1. Add Password")
        print("2. View Saved Passwords")
        print("3. Delete a Password")
        print("4. Update a Password")
        print("5. Exit")

        choice = input("Select an option: ")

        if choice == '1':
            add_password()
        elif choice == '2':
            view_passwords()
        elif choice == '3':
            delete_password()
        elif choice == '4':
            update_password()
        elif choice == '5':
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
