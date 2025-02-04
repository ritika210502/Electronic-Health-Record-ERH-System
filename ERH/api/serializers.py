from rest_framework import serializers
from .models import Patient, Record

class PatientSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = ['id', 'name', 'dob', 'age', 'gender', 'contact', 'medical_history', 'created_at']

    def get_age(self, obj):
        return obj.get_age()  # Calls get_age() method from the model

class RecordSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.name', read_only=True)

    class Meta:
        model = Record
        fields = ['id', 'patient', 'patient_name', 'diagnosis', 'treatment', 'prescribed_medications', 'doctor_notes', 'created_at', 'updated_at']
