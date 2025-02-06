from django.shortcuts import render
from rest_framework import generics,status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Patient, Record, Doctor, Availability, Appointment
from .serializers import UserSerializer, RegisterSerializer, get_tokens, PatientSerializer, RecordSerializer, DoctorSerializer, AvailabilitySerializer, AppointmentSerializer
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .tasks import send_appointment_email

# Create your views here
class Register_user(APIView):
    permission_classes=[AllowAny]
    def post(self,request):
        serializer=RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            tokens=get_tokens(user)
            return Response({'message': "✅ Registration successful!",'user':UserSerializer(user).data,'tokens':tokens},status=status.HTTP_201_CREATED)
        return Response({"error": "❌ Registration failed.","details":serializer.errors},status=status.HTTP_400_BAD_REQUEST)

class Login_user(APIView):
    permission_classes=[AllowAny]
    def post(self,request):
        username=request.data.get('username')
        password=request.data.get('password')

        if not username or not password:
            return Response({"error": "❌ Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if user:
            tokens=get_tokens(user)
            return Response({'message': "✅ Login successful!",'user':UserSerializer(user).data,'tokens':tokens},status=status.HTTP_200_OK)
        return Response({"error": "❌ Invalid username or password."}, status=status.HTTP_400_BAD_REQUEST)

class Logout_user(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"error": "❌ Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()   # Blacklist the refresh token
            return Response({"message": "✅ Logout successful."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "❌ Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)


class Profile(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'message': "✅ Profile fetched successfully.",'user': UserSerializer(request.user).data})


class Home(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {'message': 'Welcome to Electric Healthcare System'}
        return Response(content)


class Register_patient(APIView):

    permission_classes = [IsAuthenticated]

    def post(self,request):
        serializer=PatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Create_record(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        patient_id = request.data.get('patient_id')
        try:
            patient = Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            return Response({"error": "❌ Patient not found."}, status=status.HTTP_404_NOT_FOUND)


        serialzer=RecordSerializer(data=request.data)
        if serialzer.is_valid():
            serialzer.save(patient=patient)
            return Response(serialzer.data,status=status.HTTP_201_CREATED)
            
        return Response(serialzer.errors,status=status.HTTP_400_BAD_REQUEST)

class View_record(APIView):

    permission_classes = [IsAuthenticated]

    def get(self,request,patient_id):
        patient=get_object_or_404(Patient,id=patient_id)
        records=patient.records.all()

        if not records:
            return Response({"message": "❌ No records found for this patient."}, status=status.HTTP_404_NOT_FOUND)

        serializer=RecordSerializer(records,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class Update_record(APIView):

    permission_classes = [IsAuthenticated]

    def put(self,request,record_id):
        record=get_object_or_404(Record,id=record_id)
        serializer=RecordSerializer(record,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serialzer.errors,status=status.HTTP_400_BAD_REQUEST)

class Delete_record(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self,request,record_id):
        record=get_object_or_404(Record,id=record_id)
        try :
            record.delete()
            return Response({"message": f"✅ Record for {record.patient.name} deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        
        except Exception as e:
            return Response({"error": "❌ Cannot delete record"}, status=status.HTTP_400_BAD_REQUEST)

class Doctor_list(generics.ListCreateAPIView):
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]
    queryset = Doctor.objects.all()

class Slot_Available(generics.ListCreateAPIView):
    serializer_class = AvailabilitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Availability.objects.filter(doctor=self.request.user.doctor)


class Create_appointment(generics.ListCreateAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

        
    def create(self, request, *args, **kwargs):
        request.data['patient'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            send_appointment_email.delay(
                "Appointment Confirmed", "Your appointment has been booked successfully.", request.user.email
            )
            return Response({"message": "✅ Appointment booked!"}, status=status.HTTP_201_CREATED)
        return Response({"error": "❌ Failed to book appointment."}, status=status.HTTP_400_BAD_REQUEST)


class Reschedule_appointment(generics.UpdateAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]
    queryset = Appointment.objects.all()


class Cancel_appointment(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Appointment.objects.all()
