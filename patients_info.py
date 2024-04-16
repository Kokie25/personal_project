import json
import os
from uuid import uuid4


Data_file = "patients_records.json"


def save_data_to_json(data):
    """Save data to the JSON file."""
    with open(Data_file, "w") as file:
        json.dump(data, file, indent=4)


def load_data_to_json():

    if os.path.exists(Data_file):
        with open(Data_file) as file:
            return json.load(file)
    
def unique_file_no():
    
    file_no = str(uuid4())
    
    return file_no[:8]


def updating_patients_details(patient_name,identity_number,file_no,contact_details,gender,alternative_contacts,description):
    """Update the student's booking into a booking_database when successfully booked"""

    with open(Data_file, 'r') as file:
        data = json.load(file)

    new_patient = {
        "FullNames": patient_name,
        "IdentityNo":identity_number,
        "FileNo":file_no,
        "Contact_details":contact_details,
        "Alternative_contacts":alternative_contacts,
        "Gender":gender, 
        "About":description,
    }

    data['patients'].append(new_patient)
    if file_no and identity_number in data["patients"]:
        print("Patient already exist")


    with open(Data_file, 'w') as file:
        json.dump(data, file, indent=2)
    print("File successfully created")
    return data



def create_file_for_patient():

    data = load_data_to_json()
    patient_name = input("Enter patient's Name and Surname: ").title()

    while True:
        identity_number = input("Enter patient's ID: ")
        if identity_number.isdigit() and len(identity_number) == 13:

            for patient in data["patients"]:
                if identity_number == patient["IdentityNo"]:
                    print("Identity number already exists")
                break
                    
                       
            file_no = unique_file_no()
            contact_details =input("Enter contact details of the patient: ")
            alternative_contacts = input("Enter alternative contact details: ")
            gender = input("Gender(Female or Male): ")
            description = input("Reason for the patient's visit: ")

            updating_patients_details(patient_name,identity_number,file_no,contact_details,gender,alternative_contacts,description)
            break
        
        else:
            print("incorrect identity number,check the ID and try again")
            
    
if __name__ == "__main__":
    create_file_for_patient()
