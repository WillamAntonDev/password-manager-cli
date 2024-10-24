import tkinter as tk
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json

# Password generator function
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for item in range(randint(8, 10))]
    password_symbols = [choice(symbols) for item in range(randint(2, 4))]
    password_numbers = [choice(numbers) for item in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)

    print(f"Your password is: {password}")

# Save password function
def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    # Check if both the website and password fields are not empty
    if len(website.strip()) == 0 or len(password.strip()) == 0:
        messagebox.showinfo(title="Oops!", message="Please make sure all fields are filled in.")
    else:
        new_data = {website: {"email": email, "password": password}}

        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            # Update existing data with new password
            data.update(new_data)

            try:
                with open("data.json", "w") as data_file:
                    json.dump(data, data_file, indent=4)
            except Exception as e:
                print(f"Failed to update data file. Error: {str(e)}")
        finally:
            website_entry.delete(0, tk.END)
            password_entry.delete(0, tk.END)

# Find password function
def find_password():
    website = website_entry.get().strip()

    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found.")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message="No Details Found.")

# UI SETUP
window = tk.Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = tk.Canvas(height=200, width=200)
logo_img = tk.PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# Labels
website_label = tk.Label(text="Website:", width=21)
website_label.grid(row=1, column=0)
email_label = tk.Label(text="Email/Username:")
email_label.grid(row=2, column=0)
password_label = tk.Label(text="Password:")
password_label.grid(row=3, column=0)

# Entries
website_entry = tk.Entry(width=21)
website_entry.grid(row=1, column=1)
website_entry.focus()
email_entry = tk.Entry(width=35)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0, "banton65@gmail.com")
password_entry = tk.Entry(width=21)
password_entry.grid(row=3, column=1)

# Buttons
search_button = tk.Button(text="Search", width=13, command=find_password)
search_button.grid(row=1, column=2)
generate_password_button = tk.Button(text="Generate Password", command=generate_password)
generate_password_button.grid(row=3, column=2)
add_button = tk.Button(text="Add", width=36, command=save)
add_button.grid(row=4, column=1, columnspan=2)

window.mainloop()
