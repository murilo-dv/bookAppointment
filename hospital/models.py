from django.db import models
from django.contrib.auth.models import User, Group
from datetime import date
from django.utils.timezone import now
from time import time, daylight

today = now

departments=[('Cardiologist','Cardiologist'),
('Dermatologists','Dermatologists'),
('Emergency Medicine Specialists','Emergency Medicine Specialists'),
('Allergists/Immunologists','Allergists/Immunologists'),
('Anesthesiologists','Anesthesiologists'),
('Colon and Rectal Surgeons','Colon and Rectal Surgeons')
]

class Doctor(models.Model):
    id = models.AutoField(primary_key=True)
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/DoctorProfilePic/',null=True,blank=True)
    ahpra = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=True)
    department= models.CharField(max_length=50,choices=departments,default='Cardiologist')
    status=models.BooleanField(default=False)
    
    @property
    def get_name(self):
        return f"{self.user.first_name} {self.user.last_name}"
    @property
    def get_id(self):
         return self.user.id
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"



class Patient(models.Model):
    id = models.AutoField(primary_key=True)
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/PatientProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20)
    symptoms = models.CharField(max_length=100)
    medicare = models.CharField(max_length=12, null=True)
    admitDate=models.DateField(auto_now=True)
    status=models.BooleanField(default=False)
    
    @property
    def get_name(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Appointment(models.Model):
    TIMESLOT_LIST = [
        (0, '08:00 - 08:30'),
        (1, '08:30 - 09:00'),
        (2, '09:00 - 09:30'),
        (3, '10:00 - 10:30'),
        (4, '11:00 - 11:30'),
        (5, '12:00 - 12:30'),
        (6, '13:00 - 13:30'),
        (7, '14:00 - 14:30'),
        (8, '15:00 - 15:30'),
        (9, '16:00 - 16:30'),
        (10, '17:00 - 17:30'),
        (11, '17:00 - 18:00'),
    ]

    doctor = models.ForeignKey(Doctor, on_delete = models.CASCADE)
    patient = models.ForeignKey('Patient',on_delete = models.CASCADE, blank=True, null=True)
    date = models.DateField(help_text="YYYY-MM-DD")
    timeslot = models.IntegerField(choices=TIMESLOT_LIST)
    description=models.TextField(max_length=500)
    status=models.BooleanField(default=False)

    class Meta:
        unique_together = ('date', 'timeslot', 'doctor')

    def __str__(self):
        return f"Appointment with Dr. {self.doctor.get_name} on {self.date} at {self.get_timeslot_display}"

    @property
    def get_timeslot_display(self):
                # Use the `choices` tuple directly
        timeslot_dict = dict(Appointment.TIMESLOT_LIST)
        return timeslot_dict.get(self.timeslot, "Unknown Time")
    
    def save(self, *args, **kwargs):
        # Ensure that the appointment's date and time slot is available for the doctor
        if not DoctorAvailability.objects.filter(
            doctor=self.doctor, date=self.date, timeslot=self.timeslot
        ).exists():
            raise ValueError("This time slot is not available for the doctor.")
        super().save(*args, **kwargs)

class DoctorAvailability(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, default=1)
    date = models.DateField()
    timeslot = models.IntegerField(choices=Appointment.TIMESLOT_LIST)

    class Meta:
        unique_together = ('doctor', 'date', 'timeslot')

    def __str__(self):
        return f"Doctor: {self.doctor.get_name}, Date: {self.date}, Time: {self.get_timeslot_display}"
    
    @property
    def get_timeslot_display(self):
                # Use the `choices` tuple directly
        timeslot_dict = dict(Appointment.TIMESLOT_LIST)
        return timeslot_dict.get(self.timeslot, "Unknown Time")
    
    


