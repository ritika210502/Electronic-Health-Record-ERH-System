from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Patient, Record
from .serializers import PatientSerializer, RecordSerializer

# Create your views here.
class Register_patient(APIView):
    def post(self,request):
        serializer=PatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Create_record(APIView):
    def post(self,request):
        serialzer=RecordSerializer(data=request.data)
        if serialzer.is_valid():
            serialzer.save()
            return Response(serialzer.data,status=status.HTTP_201_CREATED)
        return Response(serialzer.errors,status=status.HTTP_400_BAD_REQUEST)

class View_record(APIView):
    def get(self,request,patient_id):
        patient=get_object_or_404(Patient,id=patient_id)
        records=patient.records.all()
        serializer=RecordSerializer(records,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class Update_record(APIView):
    def put(self,request,record_id):
        record=get_object_or_404(Record,id=record_id)
        serializer=RecordSerializer(record,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serialzer.errors,status=status.HTTP_400_BAD_REQUEST)

class Delete_record(APIView):
    def delete(self,request,record_id):
        record=get_object_or_404(Record,id=record_id)
        record.delete()
        return Response({"message": "Record deleted successfully"}, status=status.HTTP_204_NO_CONTENT)