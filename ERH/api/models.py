from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.timezone import now
from datetime import date

# Create your models here.
class Patient(models.Model):
    gender_choices=[
        ('M','Male'),
        ('F','Female'),
        ('T','Transgender')
    ]
    name=models.CharField(max_length=255)
    dob=models.DateField()  #taking dob instead of age
    gender=models.CharField(max_length=20,choices=gender_choices)
    contact=PhoneNumberField(unique=True)
    medical_history=models.TextField(blank=True, null=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.get_age()} years"
    
    def get_age(self):
        today=date.today()
        return today.year-self.dob.year - ((today.month, today.day)<(self.dob.month,self.dob.day))

class Record(models.Model):
    patient=models.ForeignKey(Patient,on_delete=models.CASCADE,related_name='records')
    diagnosis = models.TextField()
    treatment = models.TextField()
    prescribed_medications = models.TextField(blank=True, null=True)
    doctor_notes = models.TextField(blank=True, null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Record for {self.patient.name} - {self.created_at.date()}"

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.timezone import now

class Doctor(models.Model):
    specialties = [
        ('General', 'General Physician'),
        ('Cardio', 'Cardiologist'),
        ('Derm', 'Dermatologist'),
        ('Neuro', 'Neurologist'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=20, choices=specialties)
    contact=PhoneNumberField(unique=True)

    def __str__(self):
        return f"Dr. {self.user.username} - {self.specialty}"

class Availability(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="availabilities")
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        unique_together = ('doctor', 'date', 'start_time')

    def __str__(self):
        return f"{self.doctor.user.username} - {self.date} ({self.start_time} - {self.end_time})"

class Appointment(models.Model):
    status = [
        ('Booked', 'Booked'),
        ('Cancelled', 'Cancelled'),
        ('Completed', 'Completed'),
    ]

    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="appointments")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="appointments")
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=10, choices=status, default='Booked')

    class Meta:
        unique_together = ('doctor', 'date', 'time')
        indexes = [ models.Index(fields=['doctor', 'date', 'time']),]


    def __str__(self):
        return f"{self.patient.username} - {self.doctor.user.username} on {self.date} at {self.time}"

