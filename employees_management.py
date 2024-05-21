import json
import os
from uuid import uuid4
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from main_file import *




employees_file = "employees_logins.json"
admin_file = "admin.json"
doctors_file ="doctor_login.json"
availability_file = 'doctor_availability.json'
current_user_role = None
user_exists = False
password_correct = False



def save_employee_data_to_json(data):
    """Save data to the JSON file."""
    with open(employees_file, "w") as file:
        json.dump(data, file, indent=4)

def load_employee_data_to_json():
    if os.path.exists(employees_file):
        with open(employees_file, "r") as file:
            return json.load(file)


def save_admin_data_to_json(data):
    """Save data to the JSON file."""
    with open(admin_file, "w") as file:
        json.dump(data, file, indent=4)


def load_admin_data_to_json():
    if os.path.exists(admin_file):
        with open(admin_file, "r") as file:
            return json.load(file)


def save_dr_data_to_json(data):
    """Save data to the JSON file."""
    with open(doctors_file, "w") as file:
        json.dump(data, file, indent=4)


def load_dr_data_to_json():
    if os.path.exists(doctors_file):
        with open(doctors_file, "r") as file:
            return json.load(file)
        

def is_admin_clerk(system_username):

    admin_data = load_admin_data_to_json()
    for admin in admin_data[ "AdminAutho"]:
        if admin["username"] == system_username:
            return True
    return False

