from django.contrib import admin
from .models import Doctor,Patient,Appointment, DoctorAvailability
# Register your models here.
class DoctorAdmin(admin.ModelAdmin):
    pass
admin.site.register(Doctor, DoctorAdmin)

class PatientAdmin(admin.ModelAdmin):
    pass
admin.site.register(Patient, PatientAdmin)

class AppointmentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Appointment, AppointmentAdmin)

class AvailabilityAdmin(admin.ModelAdmin):
    pass
admin.site.register(DoctorAvailability, AvailabilityAdmin)
