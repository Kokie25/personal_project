from flask import Flask, request, render_template, redirect, url_for, flash, session
import json
import os
from uuid import uuid4

app = Flask(__name__)
app.secret_key = '200'  # Replace with your secret key for session management

def load_json(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    return {}

def save_json(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def save_employee_data(data):
    save_json(data, 'employees_logins.json')

def save_doctor_data(data):
    save_json(data, 'doctors_details.json')


def save_patient_data(data):
    save_json(data, 'patients_records.json')

def unique_file_no():
    file_no = str(uuid4())
    return file_no[:8]

def load_employee_data():
    return load_json('employees_logins.json')


def load_admin_data():
    return load_json('admin.json')

def load_doctor_data():
    return load_json('doctors_details.json')

def load_patient_data():
    return load_json('patients_records.json')

def get_patient(identity_no):
    try:
        with open('patients_records.json', 'r') as json_file:
            data = json.load(json_file)
            for patient in data.get("patients", []):
                if patient["IdentityNo"] == identity_no:
                    return patient
    except FileNotFoundError:
        flash("Data file not found.", "error")
    return None


@app.route('/')
def landing():
    return render_template('landing_page.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']

        data = load_employee_data()
        data_admin = load_admin_data()
        data_doctor = load_doctor_data()
        password_correct = False
        user_exists = False

        # Check employee credentials
        for employee in data.get('credentials', []):
            if employee['Username'] == username:
                user_exists = True
                if employee['password'] == password:
                    if '@admin' in password:
                        password_correct = True
                        session['username'] = username  # Store username in session
                        session['role'] = 'admin'
                        flash(f"{username} Logged in successfully")
                        return redirect(url_for('register_patient'))


        if not password_correct:
            # Check admin credentials
            for admin in data_admin.get('AdminAutho', []):
                if admin['admin_username'] == username:
                    user_exists = True
                    if admin['admin_password'] == password:
                        password_correct = True
                        session['username'] = username  # Store username in session
                        session['role'] = 'adminAuth'
                        flash(f"{username} Logged in successfully")
                        return redirect(url_for('employee_registration'))
                

        if not password_correct:
            # Check doctor credentials
            for doctor in data_doctor.get('Doctor', []):
                if doctor['Username'] == username:
                    user_exists = True
                    if doctor['password'] == password:
                        password_correct = True
                        if '@dr_' in password:
                            session['username'] = username  # Store username in session
                            session['role'] = 'doctor'
                            flash(f"{username} Logged in successfully")
                            return redirect(url_for('search_patient'))
                        

        if user_exists:
            flash('Invalid username or password, try again or contact the admin')
        else:
            flash('Login details do not exist, contact admin to register into the system as an employee')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()  # Clear all data in the session
    flash('You have been logged out successfully', 'info')
    return redirect(url_for('login'))


@app.route('/handle_form', methods=['POST'])
def handle_form():
    if 'username' not in session:
        return redirect(url_for('login'))  # Redirect to login if user is not logged in

    action = request.form.get('action')
    
    if action == 'register_patient':
        return redirect(url_for('register_patient'))

    if action == 'search_patient':
        return redirect(url_for('search_patient'))

    flash("Invalid action.", "error")
    return redirect(url_for('register_patient'))



@app.route('/register_patient', methods=['GET', 'POST'])
def register_patient():
    if 'username' not in session:
        return redirect(url_for('login'))  # Redirect to login if user is not logged in

    if request.method == 'POST':
        patient_data = {
            "FullNames": request.form.get('first_name', ''),
            "LastName": request.form.get('last_name', ''),
            "Title": request.form.get('title', ''),
            "IdentityNo": request.form.get('identity_no', ''),
            "Gender": request.form.get('gender', ''),
            "Physical Address": {
                "Street": request.form.get('street', ''),
                "Surburb": request.form.get('surburb', ''),
                "City": request.form.get('city', ''),
                "Zip": request.form.get('zip', '')
            },
            "Contact_details": request.form.get('contact_no', ''),
            "Email_Address": request.form.get('email', ''),
            "Alternative_contacts": request.form.get('alt_contact', ''),
            "Next_of_kin": {
                "Title": request.form.get('kin_title', ''),
                "Initials": request.form.get('kin_initials', ''),
                "First Name": request.form.get('kin_first_name', ''),
                "Last Name": request.form.get('kin_last_name', ''),
                "Contact details": request.form.get('kin_contact', '')
            },
            "Description": request.form.get('description', ''),
            "FileNo": str(uuid4())[:8],
            "Notes": request.form.get('notes', ''),
            "Vitals": {
                "Temp": request.form.get('Temp', ''),
                "HR": request.form.get('HR', ''),
                "RR": request.form.get('RR', ''),
                "BP": request.form.get('BP', ''),
                "SpO2": request.form.get('SpO2', ''),
                "Wt": request.form.get('Weight', ''),
                "Ht": request.form.get('Height', ''),
                "Pain": request.form.get('Pain', '')
            }
        }


        data = load_patient_data()
        data.setdefault("patients", []).append(patient_data)
        save_json(data,'patients_records.json')

        return redirect(url_for('register_patient'))

    is_doctor = session.get('role') == 'doctor'
    return render_template('register_patient.html', is_doctor=is_doctor)


@app.route('/search_patient', methods=['GET', 'POST'])
def search_patient():
    if request.method == 'POST':
        identityno = request.form.get('identity_no', '').strip()

        if not identityno.isdigit() or len(identityno) != 13:
            flash("Please enter a valid 13-digit ID number.", "error")
            return redirect(url_for('search_patient'))

        data = load_patient_data()
        patient = next((p for p in data.get("patients", []) if p["IdentityNo"] == identityno), None)

        if patient:
            return redirect(url_for('fill_form', identity_no=identityno))
        else:
            flash("Patient with the given ID number does not exist.", "info")
            return redirect(url_for('search_patient'))

    user_role = session.get('role', 'unknown')
    return render_template('search_patient.html', user_role=user_role)



@app.route('/fill_form/<identity_no>', methods=['GET'])
def fill_form(identity_no):
    patient = get_patient(identity_no)

    if not patient:
        flash("Patient with the given ID number does not exist.", "error")
        return redirect(url_for('search_patient'))

    is_doctor = session.get('role') == 'doctor'

    return render_template('patient_details.html', patient=patient,is_doctor=is_doctor)


# Add notes to a patient
@app.route('/add_notes', methods=['POST'])
def add_notes():
    if session.get('role') != 'doctor':
        flash("Access denied. Only doctors can add notes.", "error")
        return redirect(url_for('home'))

    identityno = request.form['identity_no'].strip()
    notes = request.form['notes'].strip()
    

    data = load_patient_data()

    for patient in data.get("patients", []):
        if patient["IdentityNo"] == identityno:
            patient["Notes"] = notes
            save_patient_data(data)
            flash("Notes added successfully.", "success")
            return redirect(url_for('search_patient'))

    flash("Patient not found.", "error")
    return redirect(url_for('search_patient'))


@app.route('/employee_registration', methods=['GET', 'POST'])
def employee_registration():
    if request.method == 'POST':
        system_username = request.form['username'].strip().title()
        system_password = request.form['password']

        new_employee = {
            "Username": system_username,
            "password": system_password,
        }

        employee_data = load_employee_data()
        doctor_data = load_doctor_data()
        pharm_data = load_pharm_data()
        

        # Check for existing username in employees
        for employee in employee_data.get("credentials", []):
            if employee["Username"] == system_username:
                flash("Username already exists")
                return redirect(url_for('employee_registration'))

        # Check for existing username in doctors
        for doctor in doctor_data.get("Doctor", []):
            if doctor["Username"] == system_username:
                flash("Username already exists")
                return redirect(url_for('employee_registration'))

        # Register as doctor or admin
        if "@dr_" in system_password:
            doctor_data.setdefault("Doctor", []).append(new_employee)
            save_doctor_data(doctor_data)
            flash("Doctor registration successful!")
            return redirect(url_for('login'))
        elif "@admin" in system_password:
            employee_data.setdefault("credentials", []).append(new_employee)
            save_employee_data(employee_data)
            flash("Admin registration successful!")
            return redirect(url_for('login'))
        else:
            flash("Incorrect password. Try again!")

        return redirect(url_for('employee_registration'))

    return render_template('employee_registration.html')



if __name__ == '__main__':
    app.run(debug=True)
