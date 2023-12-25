# create_fake_data.py
import random
from faker import Faker
from django.contrib.auth.models import User
from hospital.models import Doctor, Patient, Appointment

fake = Faker()

# Function to create a fake user
def create_fake_user():
    username = fake.user_name()
    email = fake.email()
    password = fake.password()
    user = User.objects.create_user(username=username, email=email, password=password)
    return user

# Function to create fake doctors
def create_fake_doctors(num_doctors):
    doctors = []
    for _ in range(num_doctors):
        user = create_fake_user()
        doctor = Doctor.objects.create(user=user, ahpra=fake.word(), mobile=fake.phone_number())
        doctors.append(doctor)
        print(f"Doctor created: {doctor}")
    return doctors

# Function to create fake patients
def create_fake_patients(num_patients):
    patients = []
    for _ in range(num_patients):
        user = create_fake_user()
        patient = Patient.objects.create(user=user, address=fake.address(), mobile=fake.phone_number(), symptoms=fake.text())
        patients.append(patient)
        print(f"Patient created: {patient}")
    return patients

# Function to create appointments for each patient with each doctor
def create_fake_appointments(doctors, patients):
    for doctor in doctors:
        for patient in patients:
            appointment_date = fake.date_this_year()
            timeslot = random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])  # Assuming 12 time slots
            description = fake.text()
            appointment = Appointment.objects.create(
                doctorId=doctor,
                patientId=patient,
                date=appointment_date,
                timeslot=timeslot,
                description=description,
                status=random.choice([True, False])
            )
            print(f"Appointment created: {appointment}")

# Generate fake data
num_doctors = 6
num_patients = 6

doctors = create_fake_doctors(num_doctors)
patients = create_fake_patients(num_patients)
create_fake_appointments(doctors, patients)

print("Fake data generation completed.")
