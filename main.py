# Uses the modules tkinter, random and json from the libray.
from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle

# Also uses an external module called pyperclip.
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

# Password Generator - creates a random password for a website.


def generate_password():

    # The variables contain the lists of letter, numbers and characters.
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    # These variables will randomly select either 8-10 or 2-4 items from the lists.
    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    # The items are combined into one.
    password_list = password_letters + password_symbols + password_numbers

    # The list values are then randomly mixed.
    shuffle(password_list)

    # The mixed list is then joined into a string.
    password = "".join(password_list)

    # The generated password is placed into the password_entry text field.
    password_entry.insert(0, password)

    # It is also copied to the clipboard to paste into the website.
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #

# The function saves the information entered into the fields.
def save():

    # Retrieves the website, email & password fields.
    web = web_address.get()
    address = email_entry.get()
    password = password_entry.get()

    # Creates a new dictionary created using the variables above.
    new_data = {web: {
                        "email": address,
                        "password": password,
                     }
                }

    # If any of the fields are empty a message is displayed.
    if len(web) == 0 or len(address) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty!")

    # If all fields are filled the information is added to a json file.
    else:
        try:
            # Opens the json file or creates one if it is not found.
            with open("data.json", mode="r") as data_file:
                # reading old data #
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", mode="w") as data_file:
                json.dump(new_data, data_file, indent=4)

        # Will update the information if the website is present or create a new entry.
        else:
            # Updating old data with new data #
            data.update(new_data)

            with open("data.json", "w") as data_file:
                # Saving updated data #
                json.dump(data, data_file, indent=4)

        # Will remove the entries from the website/password from the text boxes.
        finally:

            web_address.delete(0, "end")
            password_entry.delete(0, "end")


# ---------------------------- SEARCH ENTRIES ------------------------------ #

# Retrieves information from the json file using the website text box as a reference.
def find_password():

    # Retrieves the wanted website information.
    web = web_address.get()

    # Opens the json file.
    try:
        with open("data.json", mode="r") as data_file:
            # reading old data #
            data = json.load(data_file)
    # returns an error if the file is not found.
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found.")

    # Retrieves the wanted information or lets the user know it is not available.
    else:
        if web in data:
            messagebox.showinfo(title=web, message=f"Email: {data[web]['email']}\nPassword: {data[web]['password']}")
        else:
            messagebox.showinfo(title="Error", message=f"No entry for {web} found.")


# ---------------------------- UI SETUP ------------------------------- #

# Creates the window screen and all the elements that will make up the screen.
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# image #
canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# website #
web = Label(text="Website:")
web.grid(row=1, column=0, sticky="e")

# web address #
web_address = Entry(width=24)
web_address.focus()
web_address.grid(row=1, column=1, columnspan=2, sticky="w")

# email #
email = Label(text="Email/Username:")
email.grid(column=0, row=2)

# username entry #
email_entry = Entry(width=43)
email_entry.insert(0, "randomaddress@email.com")
email_entry.grid(row=2, column=1, columnspan=2, sticky="w")

# password #
password_label = Label(text="Password:")
password_label.grid(row=3, column=0, sticky="e")

# password entry #
password_entry = Entry(width=24)
password_entry.grid(row=3, column=1, columnspan=2, sticky="w")

# search #
search_button = Button(text="Search", width=14, command=find_password)
search_button.grid(row=1, column=1, columnspan=2, sticky="e")

# generate password #
generate_button = Button(text="Generate Password", width=14, command=generate_password)
generate_button.grid(row=3, column=1, columnspan=2, sticky="e")

# add to list #
add_button = Button(text="Add", width=36, command=save)
add_button.grid(row=4, column=1, columnspan=2, sticky="w")

window.mainloop()
