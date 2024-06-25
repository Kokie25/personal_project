import json
import os
from uuid import uuid4
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from main_file import *
from employees_management import *


def cancel_reg():

    if messagebox.askokcancel("Cancel", "Are you sure you want to cancel?"):
        employee_register_window.destroy()
        login_window.deiconify()

    
def employees_registration():

    
    system_username = username_entry.get().title()
    system_password = password_entry.get()

    new_employee = {
        "Username": system_username,
        "password": system_password,
    }

    employee_data = load_employee_data_to_json()
    doctor_data = load_doctor_data()

    for employee in employee_data["credentials"]:
        if employee["Username"] == system_username:
            messagebox.showerror("Registration Failed", "Username already exists")
            return

  
    for doctor in doctor_data["Doctor"]:
        if doctor["Username"] == system_username:
            messagebox.showerror("Registration Failed", "Username already exists")
            return

    if "@dr_" in system_password:
        doctor_data["Doctor"].append(new_employee)
        save_doctor_data(doctor_data)
        messagebox.showinfo("Success", "Doctor registration successful!")
        login_window.deiconify()
        employee_register_window.withdraw()

    elif "@admin" in system_password:
        employee_data["credentials"].append(new_employee)
        save_employee_data_to_json(employee_data)
        messagebox.showinfo("Success", "Admin registration successful!")
        login_window.deiconify()
        employee_register_window.withdraw()

    else:
        messagebox.showerror("Registration Failed", "Incorrect password. Try again!")



employee_register_window = Tk()
employee_register_window.title("Register")
employee_register_window.config(bg="#D8EFD3")

frame = Frame(employee_register_window, bg="#D8EFD3")
frame.pack(expand=True)

username_label = Label(frame, text="Username:", bg="#D8EFD3")
username_label.pack(pady=5)
username_entry = Entry(frame, bg="white",highlightcolor = 'grey', fg ="#393e46",highlightthickness = 1, bd=5,font='sans 10 bold')
username_entry.pack(anchor="center",pady=5)

password_label = Label(frame, text="Password:", bg="#D8EFD3")
password_label.pack(pady=5)
password_entry = Entry(frame, show="*", bg="white",highlightcolor = 'grey', fg ="#393e46",highlightthickness = 1, bd=5,font='sans 10 bold')
password_entry.pack(anchor="center",pady=5)

register_button = Button(frame, text="Register", command=employees_registration, bg="white")
register_button.pack(anchor="center",pady=5)

cancel_button = Button(frame, text="Cancel", command=cancel_reg, bg="white")
cancel_button.pack(anchor="center",pady=5)


employee_register_window.withdraw()



def login():
    
    data = load_employee_data_to_json()
    data_admin = load_admin_data_to_json()
    data_doctor = load_doctor_data()
    system_username = login_username_entry.get().title()
    system_password = login_password_entry.get()
    password_correct = False
    user_exists = False
    
   

    for employee in data.get("credentials", []):
        if employee["Username"] == system_username:
            user_exists = True
            if employee["password"] == system_password:
                password_correct = True
                messagebox.showinfo("Logged in", system_username + " Logged in successfully")
                root.deiconify()
                login_window.withdraw()
                return system_password

    if not password_correct:
        for admin in data_admin.get("AdminAutho", []):
            if admin["admin_username"] == system_username:
                user_exists = True
                if admin["admin_password"] == system_password:
                    password_correct = True
                    messagebox.showinfo("Logged in", system_username + " Logged in successfully")
                    employee_register_window.deiconify()
                    login_window.withdraw()
                    return system_password
                
    if not password_correct:
        for doctor in data_doctor.get("Doctor", []):
            if doctor["Username"] == system_username:
                user_exists = True
                if doctor["password"] == system_password:
                    password_correct = True
                    if "@dr_" in system_password:
                        Notes_text.config(state='normal')
                    messagebox.showinfo("Logged in", system_username + " Logged in successfully")
                    root.deiconify()
                    login_window.withdraw()
                    return system_password
    
    if user_exists:
        messagebox.showerror("Login Failed", "Invalid username or password, try again or contact the admin")
    else:
        messagebox.showerror("Login Failed", "Login details do not exist, contact admin to register into the system as an employee")

    return None


login_window = Tk()
login_window.title("Login")
login_window.config(bg="#95D2B3") 

frame = Frame(login_window, bg="#95D2B3")
frame.pack(expand=True)

username_label = Label(frame, text="Username:", bg="#95D2B3")
username_label.pack(anchor="center", pady=5)
login_username_entry = Entry(frame,highlightcolor = 'grey', bg='#F3FEFF',fg ="#393e46",highlightthickness = 1, bd=5,font='sans 10 bold')
login_username_entry.pack(anchor="center", pady=5)

password_label = Label(frame, text="Password:", bg="#95D2B3")
password_label.pack(anchor="center", pady=5)
login_password_entry = Entry(frame, show="*",highlightcolor = 'grey', bg='#F3FEFF',fg ="#393e46",highlightthickness = 1, bd=5,font='sans 10 bold')
login_password_entry.pack(anchor="center", pady=5)

login_button = Button(frame, text="Login", command=login)
login_button.pack(anchor="center", pady=10)



root.withdraw()
login_window.mainloop()