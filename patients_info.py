import json
import os
from uuid import uuid4
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

Data_file = "patients_records.json"

def save_data_to_json(data):
    """Save data to the JSON file."""
    with open(Data_file, "w") as file:
        json.dump(data, file, indent=4)

def load_data_to_json():
    if os.path.exists(Data_file):
        with open(Data_file, "r") as file:
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
    identityno = identity_entry.get()
    print("Got all inputs successfully...")
    
    if not identityno.isdigit() or len(str(identityno)) != 13:
        messagebox.showerror("Error", "Please enter a valid 13-digit ID number.")
        return
    notes = notes_combobox.get()
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
        "Contact details": next_of_kin_entries[4].get()
    }
    print("Created Physical Address and Next of Kin dicts...")
    
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
        "Notes": notes,
        "FileNo": file_number,
    }
    print("Created new patient dict...")

    try:
        with open(Data_file, "r") as json_file:
            data = json.load(json_file) 

    except FileNotFoundError:
        data = {"patients": []}  

    for patient in data["patients"]:
        if patient["IdentityNo"] == identityno:
            messagebox.showerror("ID No already exists")
            return  

    data["patients"].append(new_patient)
    print("Appended new patient data...")

    with open(Data_file, "w") as json_file:
        json.dump(data, json_file, indent=4)
    print("Data written to JSON file...")

    messagebox.showinfo("Success", "Registration successful!")
    print("Registration successful!")


root = Tk()
root.title("Patient Registration Form")
form_width = 500
form_height =500
root.geometry(f"{form_width}x{form_height}")
root.configure(bg="lightblue")

canvas = Canvas(root)
scrollbar = Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = Frame(canvas)

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


personal_label = Label(scrollable_frame, text="PERSONAL DETAILS", font=("Arial", 12, "bold"))
personal_label.pack(padx=10, pady=10, anchor="w")

first_name_label = Label(scrollable_frame, text="First Name:")
validate_name = root.register(validate_name_input)
first_name_label.pack(padx=10, pady=5, anchor="w")
First_name_entry = Entry(scrollable_frame, width=40,validate="key", validatecommand =(validate_name, "%P"),
                         highlightcolor = 'green', bg='#F3FEFF',fg ="#393e46",highlightthickness = 1, bd=5,font='sans 10 bold')
First_name_entry.pack(padx=10, pady=5, anchor="w")

last_name_label = Label(scrollable_frame, text="Last Name:")
last_name_label.pack(padx=10, pady=5, anchor="w")
validate_lastname = root.register(validate_name_input)
Last_name_entry = Entry(scrollable_frame, width=40,validate="key", validatecommand =(validate_lastname, "%P"),highlightcolor = 'green', bg='#F3FEFF',fg ="#393e46"
                    ,highlightthickness = 1, bd=5,font='sans 10 bold')
Last_name_entry.pack(padx=10, pady=5, anchor="w")


title_label = ttk.Label(scrollable_frame, text="Title:")
title_label.pack(padx=10, pady=5, anchor="w")
title_combobox = ttk.Combobox(scrollable_frame, values=["Mr", "Ms", "Mrs", "Miss", "Dr"],state="readonly", width=37)
title_combobox.pack(padx=10, pady=5, anchor="w")

identity_label = Label(scrollable_frame, text="SA ID number:")
identity_label.pack(padx=10, pady=5, anchor="w")
identity_entry = Entry(scrollable_frame, width=40, validate="key", validatecommand=(root.register(validate_numbers_input), "%P"),
                       highlightcolor = 'green', bg='#F3FEFF',fg ="#393e46",highlightthickness = 1, bd=5,font='sans 10 bold')
identity_entry.pack(padx=10, pady=5, anchor="w")

gender_label = Label(scrollable_frame, text="Gender:")
gender_label.pack(padx=10, pady=5, anchor="w")
gender_combobox = ttk.Combobox(scrollable_frame, values=["Male", "Female", "Other"],state="readonly", width=37)
gender_combobox.pack(padx=10, pady=5, anchor="w")

mobile_label = Label(scrollable_frame, text="Contact no:")
mobile_label.pack(padx=10, pady=5, anchor="w")
Mobile_entry = Entry(scrollable_frame, width=40)
Mobile_entry.pack(padx=10, pady=5, anchor="w")

altContact_label = Label(scrollable_frame, text="Alternative no:")
altContact_label.pack(padx=10, pady=5, anchor="w")
Alternative_contacts = Entry(scrollable_frame, width=40,validate="key", validatecommand=(root.register(validate_numbers_input), "%P"),
                             highlightcolor = 'green', bg='#F3FEFF',fg ="#393e46",highlightthickness = 1, bd=5,font='sans 10 bold')
Alternative_contacts.pack(padx=10, pady=5, anchor="w")

email_label = Label(scrollable_frame, text="Email Address:")
email_label.pack(padx=10, pady=5, anchor="w")
email_entry = Entry(scrollable_frame, width=40,highlightcolor = 'green', bg='#F3FEFF',fg ="#393e46",highlightthickness = 1, bd=5,font='sans 10 bold')
email_entry.pack(padx=10, pady=5, anchor="w")

phys_address_label = Label(scrollable_frame, text="PHYSICAL ADDRESS", font=("Arial", 12, "bold"))
phys_address_label.pack(padx=10, pady=10, anchor="w")

physical_address_labels = [
    "Street address:", "Surburb:", "City:", "Zip code:"
]
physical_address_entries = []

for label_text in physical_address_labels:
    frame = Frame(scrollable_frame)
    frame.pack(padx=10, pady=5, anchor="w")

    label = Label(frame, text=label_text)
    label.pack(side="left")

    address_entry = Entry(frame, width=37,highlightcolor = 'green', bg='#F3FEFF',fg ="#393e46",highlightthickness = 1, bd=5,font='sans 10 bold')
    address_entry.pack(side="left", padx=(10, 0))
    physical_address_entries.append(address_entry)

next_of_kin_label = Label(scrollable_frame, text="NEXT OF KIN DETAILS", font=("Arial", 12, "bold"))
next_of_kin_label.pack(padx=10, pady=10, anchor="w")

next_of_kin_labels = [
    "Title:", "Initials:", "First Name:","Last Name:","Contact details:"
]
next_of_kin_entries = []

for label_text in next_of_kin_labels:
    frame = Frame(scrollable_frame)
    frame.pack(padx=10, pady=5, anchor="w")

    label = Label(frame, text=label_text)
    label.pack(side="left")

    if label_text == "Title:":
        title_options = ["Mr", "Ms", "Mrs", "Miss", "Dr"]
        kin_entry = ttk.Combobox(frame, values=title_options, state="readonly",width=34)
    else:
        kin_entry = Entry(frame, width=37,highlightcolor = 'green', bg='#F3FEFF',fg ="#393e46",highlightthickness = 1, bd=5,font='sans 10 bold')
    
    kin_entry.pack(side="left", padx=(10, 0))
    next_of_kin_entries.append(kin_entry)


file_no = str(uuid4())[:8]  
file_label = Label(scrollable_frame, text="File No:")
file_label.pack(padx=10, pady=5, anchor="w")
File_no_entry = Entry(scrollable_frame, width=40,highlightcolor = 'green', bg='#F3FEFF', fg='black', highlightbackground='green',highlightthickness = 1, bd=5,font='sans 10 bold')

File_no_entry.insert(0, file_no)
File_no_entry.pack(padx=10, pady=5, anchor="w")

notes_label = Label(scrollable_frame, text="Description:")
notes_label.pack(padx=10, pady=5, anchor="w")
notes_combobox = ttk.Combobox(scrollable_frame, values=["Consultation", "Immunisation", "Collecting Medication","Checkup","Vaccination"],state="readonly",width=37)
notes_combobox.pack(padx=10, pady=5, anchor="w")


cancel_button = Button(scrollable_frame,text="Cancel",command = cancel_action,fg="red",bg="white",highlightbackground = "lightgrey",highlightthickness = 1, bd=5,font='sans 10 bold')
cancel_button.pack(side ="bottom",pady=10, anchor="w")


register_button = Button(scrollable_frame, text="Register", command=register,fg="green",bg="white",highlightbackground = "lightgrey",highlightthickness = 1, bd=5,font='sans 10 bold')
register_button.pack(side ="bottom",pady=10, anchor="w")



root.mainloop()
