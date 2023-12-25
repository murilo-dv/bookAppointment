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
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
         return self.user.id
    def __str__(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)



class Patient(models.Model):
    id = models.AutoField(primary_key=True)
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/PatientProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    symptoms = models.CharField(max_length=100,null=False)
    medicare = models.CharField(max_length=12, null=True)
    #assignedDoctorId = models.PositiveIntegerField(null=True)
    admitDate=models.DateField(auto_now=True)
    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name+" "+ self.user.last_name


class Appointment(models.Model):
    """Contains info about appointment"""

    class Meta:
        unique_together = ('date', 'timeslot')

    TIMESLOT_LIST = (
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
    )

    
    date = models.DateField(help_text="YYYY-MM-DD", blank=True)
    doctorId = models.ForeignKey('Doctor',on_delete = models.CASCADE, null=True, blank=True, default=None)
    patientId = models.ForeignKey('Patient',on_delete = models.CASCADE, blank=True, default=None)
    timeslot = models.IntegerField(choices=TIMESLOT_LIST, null=True)
    description=models.TextField(max_length=500)
    status=models.BooleanField(default=False)
    
    def __str__(self):
          return '{}. Patient: {}'.format( self.time, self.patientId)

    @property
    def time(self):
        return self.TIMESLOT_LIST[self.timeslot][1]


# class Appointment(models.Model):
#     patientId=models.PositiveIntegerField(null=True)
#     doctorId=models.PositiveIntegerField(null=True)
#     patientName=models.CharField(max_length=40,null=True)
#     doctorName=models.CharField(max_length=40,null=True)
#     appointmentDate=models.DateField(auto_now=True)
#     description=models.TextField(max_length=500)
#     status=models.BooleanField(default=False)

