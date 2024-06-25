import json
import os
from uuid import uuid4
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import Employees_logins_info as login
from employees_management import *


patients_records = "patients_records.json"
user1 = load_admin_data_to_json()
user2 = load_doctor_data()


def save_data_to_json(data):
    """Save data to the JSON file."""
    with open(patients_records, "w") as file:
        json.dump(data, file, indent=4)

def load_data_to_json():
    if os.path.exists(patients_records):
        with open(patients_records, "r") as file:
            return json.load(file)
        


def unique_file_no():
    file_no = str(uuid4())
    email_entry
    return file_no[:8]

def validate_numbers_input(text):
    if text.isdigit() or text == "":
        return True
    else:
        return False
    
def validate_name_input(new_value):
    return new_value.isalpha() or new_value == "" 


def cancel_action():

    if messagebox.askokcancel("Cancel", "Are you sure you want to cancel?"):
        root.destroy()
    
        return

   
def search_patient():

    identityno = identity_entry.get()

    
    if not identityno.isdigit() or len(str(identityno)) != 13:
        messagebox.showerror("Error", "Please enter a valid 13-digit ID number.")
        return
    
    try:
        with open(patients_records, "r") as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        messagebox.showerror("Error", "Data file not found.")
        return
    
    for patient in data["patients"]:
        if patient["IdentityNo"] == identityno:
            fill_form(patient)
            return
    
    messagebox.showinfo("Not Found", "Patient with the given ID number does not exist.")

def fill_form(patient):
    
    system_password = login.login()

    First_name_entry.delete(0, END)
    First_name_entry.insert(0, patient["FullNames"])
    Last_name_entry.delete(0, END)
    Last_name_entry.insert(0, patient["LastName"])
    title_combobox.set(patient["Title"])
    gender_combobox.set(patient["Gender"])
    File_no_entry.delete(0, END)
    File_no_entry.insert(0, patient["FileNo"])
    email_entry.delete(0, END)
    email_entry.insert(0, patient["Email_Address"])
    Mobile_entry.delete(0, END)
    Mobile_entry.insert(0, patient["Contact_details"])
    Alternative_contacts.delete(0, END)
    Alternative_contacts.insert(0, patient["Alternative_contacts"])
    notes_combobox.set(patient["Description"])

    Notes_text.config(state='normal') 
    Notes_text.delete(1.0, END)
    Notes_text.insert(1.0, patient["Notes"])
    
    if "@dr_" in system_password:
        Notes_text.config(state='normal')
    else:
        Notes_text.config(state='disabled')
            
        
    physical_address_entries[0].delete(0, END)
    physical_address_entries[0].insert(0, patient["Physical Address"]["Street"])
    physical_address_entries[1].delete(0, END)
    physical_address_entries[1].insert(0, patient["Physical Address"]["Surburb"])
    physical_address_entries[2].delete(0, END)
    physical_address_entries[2].insert(0, patient["Physical Address"]["City"])
    physical_address_entries[3].delete(0, END)
    physical_address_entries[3].insert(0, patient["Physical Address"]["Zip"])

    next_of_kin_entries[0].set(patient["Next_of_kin"]["Title"])    
    next_of_kin_entries[1].insert(0, patient["Next_of_kin"]["Initials"])
    next_of_kin_entries[2].delete(0, END)
    next_of_kin_entries[2].insert(0, patient["Next_of_kin"]["First Name"])
    next_of_kin_entries[3].delete(0, END)
    next_of_kin_entries[3].insert(0, patient["Next_of_kin"]["Last Name"])
    next_of_kin_entries[4].delete(0, END)
    next_of_kin_entries[4].insert(0, patient["Next_of_kin"]["Contact details"])

def add_notes():

    identityno = identity_entry.get()
    
    try:
        with open(patients_records, "r") as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        messagebox.showerror("Error", "Data file not found.")
        return
    
    
    for patient in data["patients"]:
        if patient["IdentityNo"] == identityno:
            
            patient["Notes"] = Notes_text.get("1.0", "end-1c")
            
            with open(patients_records, "w") as json_file:
                json.dump(data, json_file, indent=4)
            
            messagebox.showinfo("Success", "Notes added successfully.")
            return
    
    messagebox.showerror("Error", "Patient not found.")


def register():
    
    print("Getting user input...")
    patient_name = First_name_entry.get()
    last_name = Last_name_entry.get()
    title = title_combobox.get()
    gender = gender_combobox.get()
    file_number = File_no_entry.get()
    email = email_entry.get()
    Mobile = Mobile_entry.get()
    if not Mobile.isdigit() or len(str(Mobile)) != 10:
        messagebox.showerror("Error", "Please enter a valid 10-digit contact numbers.")
        return
    alternative_contacts = Alternative_contacts.get()
    if not alternative_contacts.isdigit() or len(str(alternative_contacts)) != 10:
        messagebox.showerror("Error", "Please enter a valid 10-digit aternative numbers.")
        return
    identityno = identity_entry.get()
    print("Got all inputs successfully...")
    
    if not identityno.isdigit() or len(str(identityno)) != 13:
        messagebox.showerror("Error", "Please enter a valid 13-digit ID number.")
        return
    description= notes_combobox.get()
    Physical_Address = {
        "Street": physical_address_entries[0].get(),
        "Surburb": physical_address_entries[1].get(),
        "City": physical_address_entries[2].get(),
        "Zip": physical_address_entries[3].get()
    }

    Next_of_kin = {
        "Title": next_of_kin_entries[0].get(),
        "Initials": next_of_kin_entries[1].get(),
        "First Name": next_of_kin_entries[2].get(),
        "Last Name":next_of_kin_entries[3].get(),
        "Contact details": next_of_kin_entries[4].get()[:10]
        
    }
    print("Created Physical Address and Next of Kin dicts...")
    Notes = Notes_text.get("1.0", "end-1c")
   
    
    new_patient = {
        "FullNames": patient_name,
        "LastName": last_name,
        "Title": title,
        "IdentityNo": identityno,
        "Gender": gender,
        "Physical Address": Physical_Address,
        "Contact_details": Mobile,
        "Email_Address": email,
        "Alternative_contacts": alternative_contacts,
        "Next_of_kin": Next_of_kin,
        "Description": description,
        "FileNo": file_number,
        "Notes":Notes
        
    }
    print("Created new patient dict...")

    try:
        with open(patients_records, "r") as json_file:
            data = json.load(json_file) 

    except FileNotFoundError:
        data = {"patients": []}  

    for patient in data["patients"]:
        if patient["IdentityNo"] == identityno:
            messagebox.showerror("ID No already exists")
            return  
    
    data["patients"].append(new_patient)
    print("Appended new patient data...")


    with open(patients_records, "w") as json_file:
        json.dump(data, json_file, indent=4)
    print("Data written to JSON file...")

    messagebox.showinfo("Success", "Registration successful!")
    print("Registration successful!")

    return identityno



root = Tk()
root.title("Patient Registration Form")
form_width = 500
form_height = 700
root.geometry(f"{form_width}x{form_height}")
root.configure(bg="#E7D4B5")

canvas = Canvas(root, bg="#E7D4B5")
scrollbar = Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = Frame(canvas, bg="#E7D4B5")

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

personal_label = Label(scrollable_frame, text="PERSONAL DETAILS", font=("Arial", 12, "bold"), bg="#E7D4B5")
personal_label.pack(padx=10, pady=10, anchor="nw")

first_name_label = Label(scrollable_frame, text="First Name:", bg="#E7D4B5")
validate_name = root.register(validate_name_input)
first_name_label.pack(padx=10, pady=5, anchor="nw")
First_name_entry = Entry(scrollable_frame, width=40, validate="key", validatecommand=(validate_name, "%P"),
                         highlightcolor='green', bg='#F3FEFF', fg="#393e46", highlightthickness=1, bd=5, font='sans 10 bold')
First_name_entry.pack(padx=10, pady=5, anchor="nw")

last_name_label = Label(scrollable_frame, text="Last Name:", bg="#E7D4B5")
last_name_label.pack(padx=10, pady=5, anchor="nw")
validate_lastname = root.register(validate_name_input)
Last_name_entry = Entry(scrollable_frame, width=40, validate="key", validatecommand=(validate_lastname, "%P"),
                        highlightcolor='green', bg='#F3FEFF', fg="#393e46", highlightthickness=1, bd=5, font='sans 10 bold')
Last_name_entry.pack(padx=10, pady=5, anchor="nw")

title_label = ttk.Label(scrollable_frame, text="Title:", background="#E7D4B5")
title_label.pack(padx=10, pady=5, anchor="nw")
title_combobox = ttk.Combobox(scrollable_frame, values=["Mr", "Ms", "Mrs", "Miss", "Dr"], state="readonly", width=37)
title_combobox.pack(padx=10, pady=5, anchor="nw")

identity_label = Label(scrollable_frame, text="SA ID number:", bg="#E7D4B5")
identity_label.pack(padx=10, pady=5, anchor="nw")
identity_entry = Entry(scrollable_frame, width=40, validate="key", validatecommand=(root.register(validate_numbers_input), "%P"),
                       highlightcolor='green', bg='#F3FEFF', fg="#393e46", highlightthickness=1, bd=5, font='sans 10 bold')
identity_entry.pack(padx=10, pady=5, anchor="nw")

gender_label = Label(scrollable_frame, text="Gender:", bg="#E7D4B5")
gender_label.pack(padx=10, pady=5, anchor="nw")
gender_combobox = ttk.Combobox(scrollable_frame, values=["Male", "Female", "Other"], state="readonly", width=37)
gender_combobox.pack(padx=10, pady=5, anchor="nw")

mobile_label = Label(scrollable_frame, text="Contact no:", bg="#E7D4B5")
mobile_label.pack(padx=10, pady=5, anchor="nw")
Mobile_entry = Entry(scrollable_frame, width=40, validate="key", validatecommand=(root.register(validate_numbers_input), "%P"),
                     highlightcolor='green', bg='#F3FEFF', fg="#393e46", highlightthickness=1, bd=5, font='sans 10 bold')
Mobile_entry.pack(padx=10, pady=5, anchor="nw")

altContact_label = Label(scrollable_frame, text="Alternative no:", bg="#E7D4B5")
altContact_label.pack(padx=10, pady=5, anchor="nw")
Alternative_contacts = Entry(scrollable_frame, width=40, validate="key", validatecommand=(root.register(validate_numbers_input), "%P"),
                             highlightcolor='green', bg='#F3FEFF', fg="#393e46", highlightthickness=1, bd=5, font='sans 10 bold')
Alternative_contacts.pack(padx=10, pady=5, anchor="nw")

email_label = Label(scrollable_frame, text="Email Address:", bg="#E7D4B5")
email_label.pack(padx=10, pady=5, anchor="nw")
email_entry = Entry(scrollable_frame, width=40, highlightcolor='green', bg='#F3FEFF', fg="#393e46", highlightthickness=1, bd=5, font='sans 10 bold')
email_entry.pack(padx=10, pady=5, anchor="nw")

phys_address_label = Label(scrollable_frame, text="PHYSICAL ADDRESS", font=("Arial", 12, "bold"), bg="#E7D4B5")
phys_address_label.pack(padx=10, pady=10, anchor="nw")

physical_address_labels = [
    "Street address:", "Surburb:", "City:", "Zip code:"
]
physical_address_entries = []

for label_text in physical_address_labels:
    frame = Frame(scrollable_frame, bg="#E7D4B5")
    frame.pack(padx=10, pady=5, anchor="nw")

    label = Label(frame, text=label_text, bg="#E7D4B5")
    label.pack(side="left")

    address_entry = Entry(frame, width=37, highlightcolor='green', bg='#F3FEFF', fg="#393e46", highlightthickness=1, bd=5, font='sans 10 bold')
    address_entry.pack(side="left", padx=(10, 0))
    physical_address_entries.append(address_entry)

next_of_kin_label = Label(scrollable_frame, text="NEXT OF KIN DETAILS", font=("Arial", 12, "bold"), bg="#E7D4B5")
next_of_kin_label.pack(padx=10, pady=10, anchor="nw")

next_of_kin_labels = [
    "Title:", "Initials:", "First Name:", "Last Name:", "Contact details:"
]
next_of_kin_entries = []

for label_text in next_of_kin_labels:
    frame = Frame(scrollable_frame, bg="#E7D4B5")
    frame.pack(padx=10, pady=5, anchor="nw")

    label = Label(frame, text=label_text, bg="#E7D4B5")
    label.pack(side="left")

    if label_text == "Title:":
        title_options = ["Mr", "Ms", "Mrs", "Miss", "Dr"]
        kin_entry = ttk.Combobox(frame, values=title_options, state="readonly", width=34)
    else:
        kin_entry = Entry(frame, width=37, highlightcolor='green', bg='#F3FEFF', fg="#393e46", highlightthickness=1, bd=5, font='sans 10 bold')
        if label_text == "Contact details:":
            kin_entry = Entry(frame, width=37, validate="key", validatecommand=(root.register(validate_numbers_input), "%P"),
                              highlightcolor='green', bg='#F3FEFF', fg="#393e46", highlightthickness=1, bd=5, font='sans 10 bold')
    
    kin_entry.pack(side="left", padx=(10, 0))
    next_of_kin_entries.append(kin_entry)

file_no = str(uuid4())[:8]
file_label = Label(scrollable_frame, text="File No:", bg="#E7D4B5")
file_label.pack(padx=10, pady=5, anchor="nw")
File_no_entry = Entry(scrollable_frame, width=40, highlightcolor='green', bg='#F3FEFF', fg='black', highlightbackground='green', highlightthickness=1, bd=5, font='sans 10 bold')

File_no_entry.insert(0, file_no)
File_no_entry.pack(padx=10, pady=5, anchor="nw")

description_label = Label(scrollable_frame, text="Description:", bg="#E7D4B5")
description_label.pack(padx=10, pady=5, anchor="nw")
notes_combobox = ttk.Combobox(scrollable_frame, values=["Consultation", "Immunisation", "Collecting Medication", "Checkup", "Vaccination"], state="readonly", width=37)
notes_combobox.pack(padx=10, pady=5, anchor="nw")

notes_label = Label(scrollable_frame,text = "Notes",bg="#E7D4B5")
notes_label.pack(padx=10, pady=5, anchor="nw")
Notes_text = Text(scrollable_frame, width=40, height=10, highlightcolor='green', bg='#F3FEFF', fg='black', highlightbackground='green', highlightthickness=1, bd=5, font='sans 10 bold', state='disabled')
Notes_text.pack(padx=10, pady=5, anchor="nw")


add_notes = Button(scrollable_frame, text="Add notes", command=add_notes, fg="green", bg="white", highlightbackground="lightgrey", highlightthickness=1, bd=5, font='sans 10 bold')
add_notes.pack(side="bottom", pady=10, anchor="nw")


register_button = Button(scrollable_frame, text="Register", command=register, fg="green", bg="white", highlightbackground="lightgrey", highlightthickness=1, bd=5, font='sans 10 bold')
register_button.pack(side="bottom", pady=10, anchor="nw")

cancel_button = Button(scrollable_frame, text="Cancel", command=cancel_action, fg="red", bg="white", highlightbackground="lightgrey", highlightthickness=1, bd=5, font='sans 10 bold')
cancel_button.pack(side="bottom", pady=10, anchor="nw")

retrieve_button = Button(scrollable_frame, text="Retrieve Data", command=search_patient, fg="yellow", bg="white", highlightbackground="lightgrey", highlightthickness=1, bd=5, font='sans 10 bold')
retrieve_button.pack(side="bottom", pady=10, anchor="nw")




