
from django.contrib import admin
from django.urls import path
from hospital import views
from django.contrib.auth.views import LoginView,LogoutView


# Homepage URLS
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home_view,name='home_page'),
    path('aboutus', views.aboutus_view, name="about_us"),
    path('contactus', views.contactus_view, name='contact_us'),
    path('book_appointment', views.book_appointment, name='form'),
    path('terms', views.terms_view, name="terms"),
    path('privacy', views.privacy_view, name="privacy"),
    path('login', LoginView.as_view(template_name='hospital/adminlogin.html'), name='login'),
    path('signup', views.signup_view,name='signup'),
    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    path('logout', LogoutView.as_view(template_name='hospital/index.html'),name='logout'),
    
    #TESTANDO
    path('test', views.test_view,name='test'),
    path('doctor/<int:id>/',views.test_doctor_view, name='doctor-test' ),
    path('get_dates', views.get_dates, name='get_dates')
]

# Dashboard Admin URLs
urlpatterns += [
    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),
    path('admin-view-patient', views.admin_view_patient_view,name='admin-view-patient'),
    path('admin-doctor', views.admin_doctor_view,name='admin-doctor'),
    path('admin-view-appointment', views.admin_view_appointment_view,name='admin-view-appointment'),
    path('admin-add-appointment', views.admin_add_appointment_view,name='admin-add-appointment'),
]

# Dashboard Doctor URLs
urlpatterns += [
    path('doctor-dashboard', views.doctor_dashboard_view,name='doctor-dashboard'),
    path('doctor-doctor', views.doctor_doctor_view,name='doctor-doctor'),
    path('doctor-view-patient', views.doctor_view_patient_view,name='doctor-view-patient'), 
    path('doctor-view-appointment', views.doctor_view_appointment_view,name='doctor-view-appointment'),
    path('doctor-add-appointment', views.doctor_add_appointment_view,name='doctor-add-appointment'),
]

# Dashboard Patient URLs
urlpatterns +=[
    path('patient-dashboard', views.patient_dashboard_view,name='patient-dashboard'),
    # path('patient-appointment', views.patient_appointment_view,name='patient-appointment'),
    # path('patient-book-appointment', views.patient_book_appointment_view,name='patient-book-appointment'),
    path('patient-view-appointment', views.patient_view_appointment_view,name='patient-view-appointment'),
    path('patient-view-doctor', views.patient_view_doctor_view,name='patient-view-doctor'),
    path('patient-add-appointment', views.patient_add_appointment_view,name='patient-add-appointment'),

]




# #-------------FOR ADMIN RELATED URLS
# urlpatterns = [

#     path('admin_patient', views.admin_patient_view,name='admin_patient'),

#     path('delete-patient-from-hospital/<int:pk>', views.delete_patient_from_hospital_view,name='delete-patient-from-hospital'),
#     path('update-patient/<int:pk>', views.update_patient_view,name='update-patient'),
#     path('admin-add-patient', views.admin_add_patient_view,name='admin-add-patient'),

# ]

# #---------FOR DOCTOR RELATED URLS-------------------------------------
# urlpatterns +=[
 
#     path('doctor-delete-appointment',views.doctor_delete_appointment_view,name='doctor-delete-appointment'),
#     path('delete-appointment/<int:pk>', views.delete_appointment_view,name='delete-appointment'),
# ]

# #---------FOR PATIENT RELATED URLS-------------------------------------

