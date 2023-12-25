# Generated by Django 4.2.6 on 2023-12-04 16:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='profile_pic/PatientProfilePic/')),
                ('address', models.CharField(max_length=40)),
                ('mobile', models.CharField(max_length=20)),
                ('symptoms', models.CharField(max_length=100)),
                ('medicare', models.CharField(max_length=12, null=True)),
                ('admitDate', models.DateField(auto_now=True)),
                ('status', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='profile_pic/DoctorProfilePic/')),
                ('ahpra', models.CharField(max_length=40)),
                ('mobile', models.CharField(max_length=20, null=True)),
                ('department', models.CharField(choices=[('Cardiologist', 'Cardiologist'), ('Dermatologists', 'Dermatologists'), ('Emergency Medicine Specialists', 'Emergency Medicine Specialists'), ('Allergists/Immunologists', 'Allergists/Immunologists'), ('Anesthesiologists', 'Anesthesiologists'), ('Colon and Rectal Surgeons', 'Colon and Rectal Surgeons')], default='Cardiologist', max_length=50)),
                ('status', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('timeslot', models.IntegerField(choices=[(0, '08:00 - 08:30'), (1, '08:30 - 09:00'), (2, '09:00 - 09:30'), (3, '10:00 - 10:30'), (4, '11:00 - 11:30'), (5, '12:00 - 12:30'), (6, '13:00 - 13:30'), (7, '14:00 - 14:30'), (8, '15:00 - 15:30'), (9, '16:00 - 16:30'), (10, '17:00 - 17:30'), (11, '17:00 - 18:00')], null=True)),
                ('description', models.TextField(max_length=500)),
                ('status', models.BooleanField(default=False)),
                ('patient', models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='hospital.patient')),
            ],
            options={
                'unique_together': {('date', 'timeslot')},
            },
        ),
    ]
