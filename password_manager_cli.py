import json
import os
import pyperclip
from random import choice, randint, shuffle

DATA_FILE = "passwords.json"

def generate_password():
    letters = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
    numbers = list("0123456789")
    symbols = list("!#$%&()*+")

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    pyperclip.copy(password)
    print(f"✅ Generated password: {password} (Copied to clipboard!)")
    return password

def save_password(website, email, password):
    new_data = {website: {"email": email, "password": password}}

    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    data.update(new_data)

    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)
    print(f"💾 Saved: {website} - {email} - {password}")

def find_password(website):
    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("🚫 No data found.")
        return

    if website in data:
        creds = data[website]
        print(f"🔍 Found credentials for {website}:")
        print(f"   Email: {creds['email']}")
        print(f"   Password: {creds['password']}")
        pyperclip.copy(creds['password'])
        print("📋 Password copied to clipboard.")
    else:
        print("❌ No entry found for that website.")

def main():
    while True:
        print("\n🔐 Password Manager")
        print("1. Generate & Save New Password")
        print("2. Find Existing Password")
        print("3. Exit")

        choice = input("Select an option (1/2/3): ")

        if choice == "1":
            website = input("Website: ").strip()
            email = input("Email/Username: ").strip()
            use_generated = input("Generate password? (y/n): ").lower() == 'y'
            password = generate_password() if use_generated else input("Enter your password: ").strip()
            save_password(website, email, password)
        elif choice == "2":
            website = input("Enter website to search: ").strip()
            find_password(website)
        elif choice == "3":
            print("👋 Bye!")
            break
        else:
            print("😑 Invalid option. Try again.")

if __name__ == "__main__":
    main()
