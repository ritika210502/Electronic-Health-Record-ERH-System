from django.urls import path,include
from api.views import Register_patient,View_record,Update_record,Delete_record,Create_record
urlpatterns = [
    path('register-patient/',Register_patient.as_view(), name='register-patient'),
    path('create-record',Create_record.as_view(),name='create-record'),
    path('view-record/<int:patient_id>/',View_record.as_view(),name='view-record'),
    path('update-record/<int:record_id>/',Update_record.as_view(),name='update-record'),
    path('delete-record/<int:record_id>/',Delete_record.as_view(),name='delete-record'),
]


