from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
gender_choices=(('M','Male'),('F','Female'),('T','Transgender'))
class Patient(models.Model):
    name=models.CharField(max_length=255)
    dob=models.DateField()  #taking dob instead of age
    gender=models.CharField(max_length=20,choices=gender_choices)
    contact=models.models.PhoneNumberField(unique=True)
    medical_history=models.TextField(blank=True, null=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.age} years"
    
    def age(self):
        today=date.today()
        return today.year-self.dob.year - ((today.month, today.day)<(self.dob.month,slef.dob.day))

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


