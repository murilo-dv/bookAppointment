from django.core.management.base import BaseCommand
from faker import Faker
from hospital.models import Doctor, Patient, Appointment, DoctorAvailability
from django.contrib.auth.models import User
import random
from django.db import IntegrityError

fake = Faker()

class Command(BaseCommand):
    help = 'Populate the database with fake data'

    def handle(self, *args, **kwargs):
        

        self.populate_doctors(10)
        self.populate_patients(10)
        self.populate_doctor_availabilities(30)
        self.populate_appointments(20)

    def populate_doctors(self, n):
        for _ in range(n):
            user = User.objects.create_user(
                username=fake.user_name(),
                password='12345Doctor',
                first_name=fake.first_name(),
                last_name=fake.last_name()
            )
            Doctor.objects.create(
                user=user,
                profile_pic='profile_pic/DoctorProfilePic/default.jpg',
                ahpra=fake.bothify(text='#######'),
                mobile=fake.phone_number(),
                department=random.choice([d[0] for d in Doctor._meta.get_field('department').choices]),
                status=True
            )
            self.stdout.write(self.style.SUCCESS('Created doctor'))

    def populate_patients(self, n):
        for _ in range(n):
            user = User.objects.create_user(
                username=fake.user_name(),
                password='12345Patient',
                first_name=fake.first_name(),
                last_name=fake.last_name()
            )
            Patient.objects.create(
                user=user,
                profile_pic='profile_pic/PatientProfilePic/default.jpg',
                address=fake.address(),
                mobile=fake.phone_number(),
                symptoms=fake.sentence(),
                medicare=fake.bothify(text='##########'),
                admitDate=fake.date(),
                status=fake.boolean()
            )
            self.stdout.write(self.style.SUCCESS('Created patient'))

    def populate_doctor_availabilities(self, n):
        doctors = Doctor.objects.all()
        for _ in range(n):
            DoctorAvailability.objects.create(
                doctor=random.choice(doctors),
                date=fake.date_this_year(),
                timeslot=random.choice([t[0] for t in Appointment.TIMESLOT_LIST])
            )
            self.stdout.write(self.style.SUCCESS('Created doctor availability'))
            
    def populate_appointments(self, n):
        doctors = Doctor.objects.all()
        patients = Patient.objects.all()
        availabilities = DoctorAvailability.objects.all()
        for _ in range(n):
            # Choose a random availability to create an appointment
            availability = random.choice(availabilities)
            try:
                Appointment.objects.create(
                    doctor=availability.doctor,
                    patient=random.choice(patients),
                    date=availability.date,
                    timeslot=availability.timeslot,
                    description=fake.text(max_nb_chars=200),
                    status=fake.boolean()
                )
                self.stdout.write(self.style.SUCCESS('Created appointment'))
            except IntegrityError:
                self.stdout.write(self.style.WARNING('Appointment already exists and was skipped'))

    
