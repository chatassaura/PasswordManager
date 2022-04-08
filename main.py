from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    # Password Generator Project
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_numbers + password_letters + password_symbols
    shuffle(password_list)
    password = "".join(password_list)
    txt_password.delete(0, END)
    txt_password.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    email = txt_email_user.get()
    website = txt_website.get().title()
    password = txt_password.get()

    new_data = {website: {
        "email": email,
        "password": password
    }}

    if len(email) == 0 or len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Warning", message="There is one or more blank information, fill to proceed !")
    else:
        try:
            data_file = open("data.json", "r")
            # read old data
            data = json.load(data_file)
            data_file.close()

        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                # Saving update data
                json.dump(new_data, data_file, indent=4)

        else:
            data.update(new_data)
            # updating old data with new data
            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            txt_website.delete(0, END)
            txt_email_user.delete(0, END)
            txt_password.delete(0, END)
            txt_website.focus()


# ---------------------------- SEARCH ------------------------------- #
def find_password():
    website = txt_website.get().title()
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Erro", message="No Data File Found.")
    else:
        if website in data:
            email = data[website]['email']
            password = data[website]['password']
            messagebox.showinfo(title=website, message=f'E-mail: {email}\nPassword: {password}')
        else:
            messagebox.showinfo(title="Error", message=f'No datails for {website} existis.')


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title('Password Manager')
window.config(padx=50, pady=50)
canvas = Canvas(width=200, height=200)
lock_img = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=lock_img)
canvas.grid(column=0, row=0, columnspan=3)

lbl_website = Label(text='Website: ')
lbl_website.grid(column=0, row=1, sticky="e", pady=3)
txt_website = Entry(width=33)
txt_website.grid(column=1, row=1, columnspan=2, sticky="w", pady=3)
txt_website.focus()

btn_search = Button(text='Search', width=20, command=find_password)
btn_search.grid(column=2, row=1)

lbl_email_user = Label(text='Email/Username: ')
lbl_email_user.grid(column=0, row=2, sticky="w", pady=3)
txt_email_user = Entry(width=58)
txt_email_user.grid(column=1, row=2, columnspan=2, sticky="w", pady=3)
# txt_email_user.insert(0, "feehssm@live.com")

lbl_password = Label(text='Password: ')
lbl_password.grid(column=0, row=3, sticky="e", pady=3)
txt_password = Entry(width=33)
txt_password.grid(column=1, row=3, sticky="w", pady=3)

btn_generate = Button(text='Generate Password', width=20, command=generate_password)
btn_generate.grid(column=2, row=3)

btn_add = Button(text='Add', width=50, command=save)
btn_add.grid(column=1, row=4, columnspan=2, sticky="w", pady=3)

window.mainloop()
