from django.shortcuts import render,redirect,reverse, get_object_or_404
from . import forms, models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import datetime,timedelta,date
from django.conf import settings
from django.db.models import Q
from datetime import date
from django.utils import timezone

today = date.today()
current_week = datetime.now().isocalendar()[1]
current_datetime = timezone.now()
month = date.today().month

# Calculate the current time as a datetime.time object
current_time = current_datetime.time()
formatted_current_time = current_time.strftime('%H:%M')
current_time_minutes = sum(map(int, formatted_current_time.split(':')))


def home_view(request):
    return render(request,'hospital/index.html')

def aboutus_view(request):
    return render(request,'hospital/aboutus.html')

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'hospital/contactussuccess.html')
    return render(request, 'hospital/contactus.html', {'form':sub})

def book_appointment(request):
  if request.method == "POST":
    form = forms.MyForm(request.POST)
    if form.is_valid():
      form.save()
  else:
      form = forms.MyForm()
  return render(request, 'hospital/book_appointment.html', {'form': form})

def terms_view(request):
    return render(request, 'hospital/terms.html')

def privacy_view(request):
    return render(request, 'hospital/privacy.html')

def signup_view(request):
    userForm=forms.PatientUserForm()
    patientForm=forms.PatientForm()
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST)
        patientForm=forms.PatientForm(request.POST,request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            patient=patientForm.save(commit=False)
            patient.user=user
            patient.assigneddoctor=request.POST.get('assigneddoctor')
            patient=patient.save()
            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)
        return HttpResponseRedirect('login')
    return render(request,'hospital/signup.html',context=mydict)

def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def is_doctor(user):
    return user.groups.filter(name='DOCTOR').exists()
def is_patient(user):
    return user.groups.filter(name='PATIENT').exists()

def afterlogin_view(request):
    if is_admin(request.user):
        return redirect('admin-dashboard')
    elif is_doctor(request.user):
        return redirect('doctor-dashboard')
    elif is_patient(request.user):
        return redirect('patient-dashboard')


###########
## ADMIN ##
###########


@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    #for both table in admin dashboard
    current_user = request.user
    doctors=models.Doctor.objects.all().order_by('-id')
    patients=models.Patient.objects.all().order_by('-id')
    todayAppointments = models.Appointment.objects.all().filter(date=today).count()
    weekAppointments = models.Appointment.objects.all().filter(date__week=current_week).count()
    monthAppointments =  models.Appointment.objects.all().filter(date__month=month).count()
    # #for three cards
    doctorcount=models.Doctor.objects.all().filter(status=True).count()
    patientcount=models.Patient.objects.all().filter(status=True).count()
    appointmentcount=models.Appointment.objects.all().filter(status=True).count()
    mydict={
    'doctors':doctors,
    'patients':patients,
    'doctorcount':doctorcount,
    'patientcount':patientcount,
    'appointmentcount':appointmentcount,
    'current_user': current_user,
    'todayAppointments':todayAppointments,
    'monthAppointments':monthAppointments,
    'weekAppointments': weekAppointments,
    'user_role': 'admin'
    }
    return render(request,'hospital/admin_dashboard.html',context=mydict)



@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_view_patient_view(request):
    patients=models.Patient.objects.all().filter(status=True)
    return render(request,'hospital/admin_view_patient.html',{'patients':patients, 'user_role': 'admin'})


@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_doctor_view(request):
    return render(request,'hospital/admin_doctor.html',{'user_role': 'admin'})

@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_view_appointment_view(request):
    appointments=models.Appointment.objects.all().filter(status=True)
    return render(request,'hospital/admin_view_appointment.html',{'appointments':appointments, 'user_role': 'admin'})

@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_add_appointment_view(request):
    appointmentForm=forms.MyForm()
    mydict={'appointmentForm':appointmentForm,'user_role': 'admin'}
    if request.method=='POST':
        appointmentForm=forms.MyForm(request.POST)
        if appointmentForm.is_valid():
            appointment=appointmentForm.save(commit=False)
            appointment.doctor=request.POST.get('doctor')
            appointment.patientId=request.POST.get('patientId')
            appointment.doctorName=models.User.objects.get(id=request.POST.get('doctor')).first_name
            appointment.patientName=models.User.objects.get(id=request.POST.get('patientId')).first_name
            appointment.status=True
            appointment.save()
        return HttpResponseRedirect('admin-view-appointment')
    return render(request,'hospital/admin_add_appointment.html',context=mydict)



############
## DOCTOR ##
############

@login_required(login_url='login')
@user_passes_test(is_doctor)
def doctor_dashboard_view(request):
    current_user = request.user
    logged_in_doctor = models.Doctor.objects.get(user=request.user)
    appointments_doctor = models.Appointment.objects.all().filter(date__gte=today, doctor=logged_in_doctor)
    todayAppointments = models.Appointment.objects.all().filter(date=today, doctor=logged_in_doctor).count()
    weekAppointments = models.Appointment.objects.all().filter(date__week=current_week, doctor=logged_in_doctor).count()
    monthAppointments =  models.Appointment.objects.all().filter(date__month=month, doctor=logged_in_doctor).count()
    next_patient_appointment = models.Appointment.objects.filter(
    doctor=logged_in_doctor,
    date__gte=current_datetime.date(),
    timeslot__gte=8
).order_by('date', 'timeslot').first()
    mydict={
    'current_user': current_user,
    'todayAppointments':todayAppointments,
    'monthAppointments':monthAppointments,
    'weekAppointments': weekAppointments,
    'next_patient_appointment':next_patient_appointment,
    'appointments_doctor':appointments_doctor,
    'user_role': 'doctor'
    }
    return render(request,'hospital/doctor_dashboard.html', context=mydict)

@login_required(login_url='login')
@user_passes_test(is_doctor)
def doctor_view_patient_view(request):
    logged_in_doctor = models.Doctor.objects.get(user=request.user)
    patients=models.Appointment.objects.all().filter(status=True, doctor=logged_in_doctor)
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'hospital/doctor_view_patient.html',{'patients':patients,'doctor':doctor, 'user_role': 'doctor'})

@login_required(login_url='login')
@user_passes_test(is_doctor)
def doctor_view_appointment_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,doctor=request.user.id)
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
    appointments=zip(appointments,patients)
    return render(request,'hospital/doctor_view_appointment.html',{'appointments':appointments,'doctor':doctor,'user_role': 'doctor'})

@login_required(login_url='login')
@user_passes_test(is_doctor)
def doctor_doctor_view(request):
    return render(request,'hospital/admin_doctor.html',{'user_role': 'doctor'})

@login_required(login_url='login')
@user_passes_test(is_doctor)
def doctor_add_appointment_view(request):
    appointmentForm=forms.MyForm()
    mydict={'appointmentForm':appointmentForm,'user_role': 'doctor'}
    if request.method=='POST':
        appointmentForm=forms.MyForm(request.POST)
        if appointmentForm.is_valid():
            appointment=appointmentForm.save(commit=False)
            appointment.doctor=request.POST.get('doctor')
            appointment.patientId=request.POST.get('patientId')
            appointment.doctorName=models.User.objects.get(id=request.POST.get('doctor')).first_name
            appointment.patientName=models.User.objects.get(id=request.POST.get('patientId')).first_name
            appointment.status=True
            appointment.save()
        return HttpResponseRedirect('doctor-view-appointment')
    return render(request,'hospital/doctor_add_appointment.html',context=mydict)

#############
## PATIENT ##
#############

@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_dashboard_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id)
    current_user = request.user
    mydict={
    'patient':patient,
    'symptoms':patient.symptoms,
    'admitDate':patient.admitDate,
    'current_user': current_user,
    'user_role': 'patient'
    }
    return render(request,'hospital/patient_dashboard.html',context=mydict)

def patient_view_doctor_view(request):
    doctors=models.Doctor.objects.all().filter(status=True)
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    user_role= 'patient'
    return render(request,'hospital/patient_view_doctor.html',{'patient':patient,'doctors':doctors, 'user_role': 'patient'})

@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_view_appointment_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    appointments=models.Appointment.objects.all().filter(patientId=request.user.id)
    return render(request,'hospital/patient_view_appointment.html',{'appointments':appointments,'patient':patient, 'user_role': 'patient'})

@login_required(login_url='login')
@user_passes_test(is_patient)
def patient_add_appointment_view(request):
    appointmentForm=forms.PatientAppointmentForm()
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    message=None
    mydict={'appointmentForm':appointmentForm,'patient':patient,'message':message, 'user_role': 'patient'}
    if request.method=='POST':
        appointmentForm=forms.PatientAppointmentForm(request.POST)
        if appointmentForm.is_valid():
            print(request.POST.get('doctor'))
            desc=request.POST.get('description')

            doctor=models.Doctor.objects.get(user_id=request.POST.get('doctor'))
            
            appointment=appointmentForm.save(commit=False)
            appointment.doctor=request.POST.get('doctor')
            appointment.patientId=request.user.id #----user can choose any patient but only their info will be stored
            appointment.doctorName=models.User.objects.get(id=request.POST.get('doctor')).first_name
            appointment.patientName=request.user.first_name #----user can choose any patient but only their info will be stored
            appointment.status=False
            appointment.save()
        return HttpResponseRedirect('patient-view-appointment')
    return render(request,'hospital/patient_book_appointment.html',context=mydict)



###########
## TESTS ##
########### 

##TESTANDO FILTROS
def test_view(request):
    all_doctors=models.Doctor.objects.all().filter(status=True)
    all_patients=models.Patient.objects.all()
    return render (request,'hospital/test.html', {'doctors': all_doctors, 'patients': all_patients})

## Get details about doctor by ID
def test_doctor_view(request, id):
    doctor = get_object_or_404(models.Doctor, user=id)
    #ids = [doctor.get_id for doctor in all_doctors]
    mydict={
        'id': doctor.get_id,
        'firstName': doctor.user.first_name,
        'lastName': doctor.user.last_name,
        'mobile': doctor.mobile,
    }
    return JsonResponse(mydict)
    #return HttpResponse (doctor.user.first_name)

## Calendar test
def get_dates(request):
    today = datetime.now()
    days_of_week = [(today + timedelta(days=i)).strftime('%A - %d/%m') for i in range(7)]
    return render(request, 'hospital/days_of_week.html', {'days_of_week': days_of_week})




# #Book Appointment
# def book_appointment(request):
#     return render(request, 'hospital/book_appointment.html')







# #for showing signup/login button for admin
# # def adminclick_view(request):
# #     if request.user.is_authenticated:
# #         return HttpResponseRedirect('afterlogin')
# #     return render(request,'hospital/adminclick.html')


# #for showing signup/login button for doctor
# # def doctorclick_view(request):
# #     if request.user.is_authenticated:
# #         return HttpResponseRedirect('afterlogin')
# #     return render(request,'hospital/doctorclick.html')


# #for showing signup/login button for patient
# # def patientclick_view(request):
# #     if request.user.is_authenticated:
# #         return HttpResponseRedirect('afterlogin')
# #     return render(request,'hospital/patientclick.html')


# # ----------Signups--------------------------






# def create_account(request):
#     if request.method == "POST":
#         form = forms.PatientNewAccount(request.POST)
#         if form.is_valid():
#             form.save()
#     else:
#       form = forms.PatientNewAccount()
#     return render(request, 'hospital/components/create_account.html', {'form': form})

# def register_patient(request):
#     if request.method == 'POST':
#         form = forms.PatientRegistrationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             # Redirect to a success page or any other desired page
#             return redirect('success_page')
#     else:
#         form = forms.PatientRegistrationForm()

#     return render(request, 'hospital/components/create_account.html', {'form': form})




# #-----------------------------------------------










# @login_required(login_url='adminlogin')
# @user_passes_test(is_admin)
# def admin_view_doctor_view(request):
#     doctors=models.Doctor.objects.all().filter(status=True)
#     return render(request,'hospital/admin_view_doctor.html',{'doctors':doctors})




# @login_required(login_url='adminlogin')
# @user_passes_test(is_admin)
# def admin_patient_view(request):
#     return render(request,'hospital/admin_patient.html')







# @login_required(login_url='adminlogin')
# @user_passes_test(is_admin)
# def delete_patient_from_hospital_view(request,pk):
#     patient=models.Patient.objects.get(id=pk)
#     user=models.User.objects.get(id=patient.user_id)
#     user.delete()
#     patient.delete()
#     return redirect('admin-view-patient')



# @login_required(login_url='adminlogin')
# @user_passes_test(is_admin)
# def update_patient_view(request,pk):
#     patient=models.Patient.objects.get(id=pk)
#     user=models.User.objects.get(id=patient.user_id)

#     userForm=forms.PatientUserForm(instance=user)
#     patientForm=forms.PatientForm(request.FILES,instance=patient)
#     mydict={'userForm':userForm,'patientForm':patientForm}
#     if request.method=='POST':
#         userForm=forms.PatientUserForm(request.POST,instance=user)
#         patientForm=forms.PatientForm(request.POST,request.FILES,instance=patient)
#         if userForm.is_valid() and patientForm.is_valid():
#             user=userForm.save()
#             user.set_password(user.password)
#             user.save()
#             patient=patientForm.save(commit=False)
#             patient.status=True
#             patient.assigneddoctor=request.POST.get('assigneddoctor')
#             patient.save()
#             return redirect('admin-view-patient')
#     return render(request,'hospital/admin_update_patient.html',context=mydict)





# @login_required(login_url='adminlogin')
# @user_passes_test(is_admin)
# def admin_add_patient_view(request):
#     userForm=forms.PatientUserForm()
#     patientForm=forms.PatientForm()
#     mydict={'userForm':userForm,'patientForm':patientForm}
#     if request.method=='POST':
#         userForm=forms.PatientUserForm(request.POST)
#         patientForm=forms.PatientForm(request.POST,request.FILES)
#         if userForm.is_valid() and patientForm.is_valid():
#             user=userForm.save()
#             user.set_password(user.password)
#             user.save()

#             patient=patientForm.save(commit=False)
#             patient.user=user
#             patient.status=True
#             patient.assigneddoctor=request.POST.get('assigneddoctor')
#             patient.save()

#             my_patient_group = Group.objects.get_or_create(name='PATIENT')
#             my_patient_group[0].user_set.add(user)

#         return HttpResponseRedirect('admin-view-patient')
#     return render(request,'hospital/admin_add_patient.html',context=mydict)





# #-----------------APPOINTMENT START--------------------------------------------------------------------
# @login_required(login_url='adminlogin')
# @user_passes_test(is_admin)
# def admin_appointment_view(request):
#     return render(request,'hospital/admin_appointment.html')














# #---------------------------------------------------------------------------------
# #------------------------ DOCTOR RELATED VIEWS START ------------------------------
# #---------------------------------------------------------------------------------




# @login_required(login_url='doctorlogin')
# @user_passes_test(is_doctor)
# def doctor_patient_view(request):
#     mydict={
#     'doctor':models.Doctor.objects.get(user_id=request.user.id), #for profile picture of doctor in sidebar
#     }
#     return render(request,'hospital/doctor_patient.html',context=mydict)








# @login_required(login_url='doctorlogin')
# @user_passes_test(is_doctor)
# def search_view(request):
#     doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
#     # whatever user write in search box we get in query
#     query = request.GET['query']
#     patients=models.Patient.objects.all().filter(status=True,assigneddoctor=request.user.id).filter(Q(symptoms__icontains=query)|Q(user__first_name__icontains=query))
#     return render(request,'hospital/doctor_view_patient.html',{'patients':patients,'doctor':doctor})



# @login_required(login_url='doctorlogin')
# @user_passes_test(is_doctor)
# def doctor_view_discharge_patient_view(request):
#     dischargedpatients=models.PatientDischargeDetails.objects.all().distinct().filter(assignedDoctorName=request.user.first_name)
#     doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
#     return render(request,'hospital/doctor_view_discharge_patient.html',{'dischargedpatients':dischargedpatients,'doctor':doctor})



# @login_required(login_url='doctorlogin')
# @user_passes_test(is_doctor)
# def doctor_appointment_view(request):
#     doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
#     return render(request,'hospital/doctor_appointment.html',{'doctor':doctor})







# @login_required(login_url='doctorlogin')
# @user_passes_test(is_doctor)
# def doctor_delete_appointment_view(request):
#     doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
#     appointments=models.Appointment.objects.all().filter(status=True,doctor=request.user.id)
#     patientid=[]
#     for a in appointments:
#         patientid.append(a.patientId)
#     patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
#     appointments=zip(appointments,patients)
#     return render(request,'hospital/doctor_delete_appointment.html',{'appointments':appointments,'doctor':doctor})



# @login_required(login_url='doctorlogin')
# @user_passes_test(is_doctor)
# def delete_appointment_view(request,pk):
#     appointment=models.Appointment.objects.get(id=pk)
#     appointment.delete()
#     doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
#     appointments=models.Appointment.objects.all().filter(status=True,doctor=request.user.id)
#     patientid=[]
#     for a in appointments:
#         patientid.append(a.patientId)
#     patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
#     appointments=zip(appointments,patients)
#     return render(request,'hospital/doctor_delete_appointment.html',{'appointments':appointments,'doctor':doctor})



# #---------------------------------------------------------------------------------
# #------------------------ DOCTOR RELATED VIEWS END ------------------------------
# #---------------------------------------------------------------------------------






# #---------------------------------------------------------------------------------
# #------------------------ PATIENT RELATED VIEWS START ------------------------------
# #---------------------------------------------------------------------------------




# @login_required(login_url='patientlogin')
# @user_passes_test(is_patient)
# def patient_appointment_view(request):
#     patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
#     return render(request,'hospital/patient_appointment.html',{'patient':patient})











# def search_doctor_view(request):
#     patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    
#     # whatever user write in search box we get in query
#     query = request.GET['query']
#     doctors=models.Doctor.objects.all().filter(status=True).filter(Q(department__icontains=query)| Q(user__first_name__icontains=query))
#     return render(request,'hospital/patient_view_doctor.html',{'patient':patient,'doctors':doctors})








# @login_required(login_url='patientlogin')
# @user_passes_test(is_patient)
# def patient_discharge_view(request):
#     patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
#     dischargeDetails=models.PatientDischargeDetails.objects.all().filter(patientId=patient.id).order_by('-id')[:1]
#     patientDict=None
#     if dischargeDetails:
#         patientDict ={
#         'is_discharged':True,
#         'patient':patient,
#         'patientId':patient.id,
#         'patientName':patient.get_name,
#         'assignedDoctorName':dischargeDetails[0].assignedDoctorName,
#         'address':patient.address,
#         'mobile':patient.mobile,
#         'symptoms':patient.symptoms,
#         'admitDate':patient.admitDate,
#         'releaseDate':dischargeDetails[0].releaseDate,
#         'daySpent':dischargeDetails[0].daySpent,
#         'medicineCost':dischargeDetails[0].medicineCost,
#         'roomCharge':dischargeDetails[0].roomCharge,
#         'doctorFee':dischargeDetails[0].doctorFee,
#         'OtherCharge':dischargeDetails[0].OtherCharge,
#         'total':dischargeDetails[0].total,
#         }
#         print(patientDict)
#     else:
#         patientDict={
#             'is_discharged':False,
#             'patient':patient,
#             'patientId':request.user.id,
#         }
#     return render(request,'hospital/patient_discharge.html',context=patientDict)


# #------------------------ PATIENT RELATED VIEWS END ------------------------------
# #---------------------------------------------------------------------------------








# #---------------------------------------------------------------------------------
# #------------------------ ABOUT US AND CONTACT US VIEWS START ------------------------------
# #---------------------------------------------------------------------------------







# #---------------------------------------------------------------------------------
# #------------------------ ADMIN RELATED VIEWS END ------------------------------
# #---------------------------------------------------------------------------------

# def admin_patient(request):
#     return render(request, 'hospital/dashboard_admin/admin_patient.html')
