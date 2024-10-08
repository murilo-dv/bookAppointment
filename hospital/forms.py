from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from . import models

# Book Appointment
class MyForm(forms.ModelForm):
  class Meta:
    model = models.Appointment
    fields = [ "doctor",  "patient", "date","timeslot", "description"]
    labels = { "doctor": "doctor name", "patient": "Patient name", "date": "Date", "timeslot":"Time", "description": "description"}
    widgets = {
        'date': forms.DateInput(attrs={
                'class': 'datepicker',  # This class will be used for targeting with Flatpickr
                'placeholder': 'Select Date',
                'type': 'date'  # Ensures the input type is date)
        })
    }


#for signup
class signup(forms.ModelForm):
    class Meta:
        model= User
        fields = ['first_name', 'last_name', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }













class DoctorForm(forms.ModelForm):
    class Meta:
        model=models.Doctor
        fields=['ahpra','mobile','department','status','profile_pic']



#for Patient related form
class PatientUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
class PatientForm(forms.ModelForm):
    #this is the extra field for linking patient and their assigend doctor
    #this will show dropdown __str__ method doctor model is shown on html so override it
    #to_field_name this will fetch corresponding value  user_id present in Doctor model and return it
    assignedDoctorId=forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True),empty_label="Name and Department", to_field_name="user_id")
    class Meta:
        model=models.Patient
        fields=['address','mobile','status','symptoms','profile_pic', 'medicare']



class AppointmentForm(forms.ModelForm):
    doctorId=forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True),empty_label="Doctor Name and Department", to_field_name="user_id")
    patientId=forms.ModelChoiceField(queryset=models.Patient.objects.all().filter(status=True),empty_label="Patient Name and Symptoms", to_field_name="user_id")
    class Meta:
        model=models.Appointment
        fields=['description','status']


class PatientAppointmentForm(forms.ModelForm):
    doctorId=forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True),empty_label="Doctor Name and Department", to_field_name="user_id")
    class Meta:
        model=models.Appointment
        fields=['description','status']


#for contact us page
class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))

class PatientNewAccount(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','first_name','last_name','password']
        widgets = {
        'password': forms.PasswordInput()
        }
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            # Get the group object
            group = Group.objects.get(name='PATIENT')
            # Add the user to the group
            user.groups.add(group)
        return user

class PatientRegistrationForm(UserCreationForm):
    address = forms.CharField(max_length=40)
    mobile = forms.CharField(max_length=20)
    symptoms = forms.CharField(max_length=100)
    medicare = forms.CharField(max_length=12)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        # Create Patient instance linked to the user
        patient = models.Patient.objects.create(
            user=user,
            address=self.cleaned_data['address'],
            mobile=self.cleaned_data['mobile'],
            symptoms=self.cleaned_data['symptoms'],
            medicare=self.cleaned_data['medicare']
        )

        # Add the user to the "PATIENT" group
        patient_group = Group.objects.get(name='PATIENT')
        user.groups.add(patient_group)

        return user
    

##########################
## VERIFY IF CAN DELETE ##
##########################


# #for admin signup
# class AdminSigupForm(forms.ModelForm):
#     class Meta:
#         model=User
#         fields=['first_name','last_name','username','password']
#         widgets = {
#         'password': forms.PasswordInput()
#         }

# #for Doctor related form
# class DoctorUserForm(forms.ModelForm):
#     class Meta:
#         model=User
#         fields=['first_name','last_name','username','password']
#         widgets = {
#         'password': forms.PasswordInput()
#         }