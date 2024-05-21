import json
import os
from uuid import uuid4
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from main_file import *
from employees_management import *




def employees_registration():

    system_username = username_entry.get().title()
    system_password = password_entry.get()
    system_role = role_combobox.get()

    new_employee = {
        "Username": system_username,
        "password": system_password,
        "Role":system_role
    }

    
    try:
        with open(employees_file, "r") as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        data = {"credentials": []}

   
    if os.path.exists(doctors_file):
        try:
            with open(doctors_file, "r") as json_file:
                doctors_data = json.load(json_file)
        except json.JSONDecodeError:
            doctors_data = {"Doctors": []}
    else:
        doctors_data = {"Doctors": []}

    
    for employee in data["credentials"]:
        if employee["Username"] == system_username and employee["password"] == system_password:
            messagebox.showerror("Registration Failed", "Username and password combination already exists")
            return

    for doctor in doctors_data["Doctors"]:
        if doctor["Username"] == system_username and doctor["password"] == system_password:
            messagebox.showerror("Registration Failed", "Username and password combination already exists in doctors database")
            return

 
        if "@admin" in system_password:
            data["credentials"].append(new_employee)
            print("Appended new employee data to employees database...")

            with open(employees_file, "w") as json_file:
                json.dump(data, json_file, indent=4)
            print("Data written to employees JSON file...")
            messagebox.showinfo("Success", "Registration successful!")
            login_window.deiconify()
            employee_register_window.withdraw()
            

        elif "@dr_" in system_password:
            doctors_data["Doctors"].append(new_employee)
            print("Appended new doctor data to doctors database...")

            with open(doctors_file, "w") as json_file:
                json.dump(doctors_data, json_file, indent=4)
            print("Data written to doctors JSON file...")
            messagebox.showinfo("Success", "Registration successful!")
            login_window.deiconify()
            employee_register_window.withdraw()


    
    else:
        if "@admin" not in system_password and "@dr_" not in system_password:
            messagebox.showerror("Registration Failed","Incorrect password.Try again!")



employee_register_window = Tk()
employee_register_window.title("Register")


username_label = Label(employee_register_window, text="Username:")
username_label.pack()
username_entry = Entry(employee_register_window)
username_entry.pack()


password_label = Label(employee_register_window, text="Password:")
password_label.pack()
password_entry = Entry(employee_register_window, show="*")  
password_entry.pack()

role_label =Label(employee_register_window,text = "Role")
role_label.pack()
role_combobox = ttk.Combobox(employee_register_window, values=["Doctor", "AdminClerk", "Administrator"],state="readonly", width=37)
role_combobox.pack()


register_button = Button(employee_register_window, text="Register", command= employees_registration)
register_button.pack()

cancel_button = Button(employee_register_window,text="Cancel",command = cancel_action)
cancel_button.pack()


employee_register_window.withdraw()

def cancel_action():

    if messagebox.askokcancel("Cancel", "Are you sure you want to cancel?"):
        root.destroy()
        employee_register_window.destroy


def login():
    global current_user_role
    data = load_employee_data_to_json()
    data_admin = load_admin_data_to_json()
    data_dr = load_dr_data_to_json()
    system_username = login_username_entry.get().title()
    system_password = login_password_entry.get()
    system_role = role_combobox.get()
    password_correct = False
    user_exists = False
    

    for employee in data.get("credentials"):
        if employee["Username"] == system_username:
            user_exists = True    
            if employee["Username"] == system_username and employee["password"] == system_password:
                password_correct = True
                current_user_role = "Employee"
                messagebox.showinfo("Logged in", system_username + " Logged in successfully")
                root.deiconify()
                login_window.withdraw()
                break

    if not password_correct:
        for admin in data_admin.get("AdminAutho"):
            if admin["admin_username"] == system_username:
                user_exists = True
                if admin["admin_username"] == system_username and admin["admin_password"] == system_password:
                    password_correct = True
                    current_user_role = "Admin"
                    messagebox.showinfo("Logged in", system_username + " Logged in successfully")
                    employee_register_window.deiconify()
                    login_window.withdraw()
                    break

    if not password_correct:
        for doctor in data_dr.get("Doctors"):
            if doctor["password"] == system_password:
                user_exists =True
                if doctor["Username"] == system_username and doctor["password"] == system_password:
                    password_correct = True
                    current_user_role = "Doctor"
                    messagebox.showinfo("Logged in", system_username + " Logged in successfully")
                    root.deiconify()
                    login_window.withdraw()
                    break
                
    if password_correct:
        if current_user_role == "Doctor":
            Notes_entry.config(state="normal")
            
        else:
            Notes_entry.config(state="disabled")
    else:
        if user_exists:
            messagebox.showerror("Login Failed", "Invalid username or password, try again or contact the admin")
        else:
            messagebox.showerror("Login Failed", "Login details do not exist, contact admin to register into the system as an employee")

    return 



login_window = Tk()
login_window.title("Login")

username_label = Label(login_window, text="Username:")
username_label.pack()
login_username_entry = Entry(login_window)
login_username_entry.pack()

password_label = Label(login_window, text="Password:")
password_label.pack()
login_password_entry = Entry(login_window, show="*")  
login_password_entry.pack()


login_button = Button(login_window, text="Login", command=login)
login_button.pack()

root.withdraw()
login_window.mainloop()