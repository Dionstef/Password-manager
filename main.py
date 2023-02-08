from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import pyperclip
import json
# ---------------------------- CONSTANTS ------------------------------- #
FONT = ("Arial", 10)
IMAGE_WIDTH = 400
IMAGE_HEIGHT = 300


# ---------------------------- PASSWORD GENERATE------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = [random.choice(letters) for _ in range(nr_letters)]
    password_list += [random.choice(symbols) for _ in range(nr_symbols)]
    password_list += [random.choice(numbers) for _ in range(nr_numbers)]

    random.shuffle(password_list)

    password = "".join(password_list)

    password_input.insert(0, password)  # Inserts password in the password entry
    pyperclip.copy(password)  # Copies password to clipboard


# ---------------------------- PASSWORD SEARCH------------------------------- #
def search_password():
    website = website_input.get()
    try:
        with open("Passwords.json", "r") as data_file:
            # Reading existing data from json
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="error", message="No Data File Found")
    else:
        # Check if website exists in file
        if website in data:
            password = data[website]['password']
            email = data[website]['email']
            pyperclip.copy(password)  # Copis password to clipboard
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: "
                                                       f"{password}\nPassword has been copied to clipboard")
        else:
            messagebox.showinfo(title="error", message=f"No Details For {website} Exist")


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_input.get()
    email = email_input.get()
    password = password_input.get()
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    if len(website) == 0 or len(password) == 0 or len(email) == 0:
        messagebox.showinfo(title="Oops", message="PLease don't leave any empty fields!")
    else:
        try:
            with open("Passwords.json", "r") as data_file:
                # Reading existing data from json
                data = json.load(data_file)
        except FileNotFoundError:
            # If file does not exist create it
            with open("Passwords.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)  # write to a json file
                messagebox.showinfo(title="File Creation", message="Passwords.json file created")
        else:
            # Update existing data with new data
            data.update(new_data)
            messagebox.showinfo(title="File Update", message="Passwords.json file updated")

            with open("Passwords.json", "w") as data_file:
                # Saving the updated data
                json.dump(data, data_file, indent=4)  # write to a json file
        finally:
            # Delete the existing values from the UI
            website_input.delete(0, 'end')
            password_input.delete(0, 'end')


# ---------------------------- UI SETUP ------------------------------- #
# Window
window = Tk()
window.title('Password Manager')
window.config(padx=50, pady=50)

# Canvas and image
load = Image.open("logo.jpg")
resize_image = load.resize((IMAGE_WIDTH, IMAGE_HEIGHT))
final_image = ImageTk.PhotoImage(resize_image)

canvas = Canvas(width=IMAGE_WIDTH, height=IMAGE_HEIGHT, borderwidth=0, highlightthickness=0)
canvas.create_image(IMAGE_WIDTH/2, IMAGE_HEIGHT/2, image=final_image)
canvas.grid(column=0, row=0, columnspan=3, pady=5)

# Labels
website = Label(text="Website: ")
website.config(font=FONT)
website.grid(column=0, row=1)

email = Label(text="Email/Username: ")
email.config(font=FONT)
email.grid(column=0, row=2)

password = Label(text="Password: ")
password.config(font=FONT)
password.grid(column=0, row=3)

# Entries
website_input = Entry(width=26)
website_input.grid(column=1, row=1, sticky="W")
website_input.focus()

email_input = Entry()
email_input.grid(column=1, row=2, columnspan=2, sticky="EW")
#email_input.insert(0, "enter you email here")  # Optional if you want a predefined e-mail

password_input = Entry(width=26)
password_input.grid(column=1, row=3, sticky="W")

# Buttons
generate_password = Button(text="Generate Password", command=generate_password)
generate_password.config(font=FONT)
generate_password.grid(column=2, row=3, sticky="EW")

add = Button(text="Add", command=save)
add.config(font=FONT)
add.grid(column=1, row=4, columnspan=2, sticky="EW")

search = Button(text="Search", command=search_password)
search.config(font=FONT)
search.grid(column=2, row=1,  sticky="EW")

window.mainloop()
