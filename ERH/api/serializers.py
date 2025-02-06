from rest_framework import serializers
from .models import Patient, Record, Doctor, Availability, Appointment
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re

def get_tokens(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8,max_length=20)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def validate_email(self, value):
        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError("❌ Invalid email format. Please enter a valid email address.")

        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("❌ This email is already registered. Try logging in or use a different email.")
        return value

    def validate_username(self, value):
        if not re.match(r'^[a-zA-Z0-9_]{3,15}$', value):
            raise serializers.ValidationError("❌ Username must be 3-15 characters long and can only contain letters, numbers, and underscores.")
        
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("❌ This username is already taken. Please choose a different one.")
        return value

    def validate_password(self, value):

        if len(value) < 8:
            raise serializers.ValidationError("❌ Password must be at least 8 characters long.")
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("❌ Password must contain at least one uppercase letter (A-Z).")
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError("❌ Password must contain at least one lowercase letter (a-z).")
        if not re.search(r'[0-9]', value):
            raise serializers.ValidationError("❌ Password must contain at least one number (0-9).")
        if not re.search(r'[@$!%*?&]', value):
            raise serializers.ValidationError("❌ Password must contain at least one special character (@, $, !, %, *, ?, &).")

        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class PatientSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = ['id', 'name', 'dob', 'age', 'gender', 'contact', 'medical_history', 'created_at']

    def get_age(self, obj):
        return obj.get_age()  # Calls get_age() method from the model
    
    def validate_name(self, value):
        if not value or value.strip() == "":
            raise serializers.ValidationError("❌ Name cannot be empty.")

        if not re.match(r'^[a-zA-Z\s]+$', value):
            raise serializers.ValidationError("❌ Name must only contain alphabetic characters and spaces.")

        if len(value) < 3:
            raise serializers.ValidationError("❌ Name must be at least 3 characters long.")
        
        return value


    def validate_dob(self, value):
        if value > timezone.now().date():
            raise serializers.ValidationError("❌ Date of birth cannot be in the future.")
        return value


class RecordSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.name', read_only=True)

    class Meta:
        model = Record
        fields = ['id', 'patient', 'patient_name', 'diagnosis', 'treatment', 'prescribed_medications', 'doctor_notes', 'created_at', 'updated_at']


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'

class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = '__all__'

    def validate(self, data):
        doctor = data['doctor']
        date = data['date']
        start_time = data['start_time']

        if Availability.objects.filter(doctor=doctor, date=date, start_time=start_time).exists():
            raise serializers.ValidationError("❌ This time slot is already booked.")
        
        return data

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'

    def validate(self, data):
        doctor = data['doctor']
        date = data['date']
        time = data['time']

        if Appointment.objects.filter(doctor=doctor, date=date, time=time).exists():
            raise serializers.ValidationError("❌ This time slot is already booked by another patient.")

        return data
