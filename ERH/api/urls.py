from django.urls import path,include
from rest_framework_simplejwt.views import TokenRefreshView
from api.views import Register_user, Login_user, Logout_user, Profile, Register_patient,View_record,Update_record,Delete_record,Create_record,Home
from api.views import Doctor_list, Slot_Available, Create_appointment, Reschedule_appointment, Cancel_appointment

urlpatterns = [
    path('register/', Register_user.as_view(), name='register'),
    path('login/', Login_user.as_view(), name='login'),
    path('profile/', Profile.as_view(), name='profile'),
    path('logout/', Logout_user.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('',Home.as_view(),name='home'),
    path('register-patient/',Register_patient.as_view(), name='register-patient'),
    path('create-record',Create_record.as_view(),name='create-record'),
    path('view-record/<int:patient_id>/',View_record.as_view(),name='view-record'),
    path('update-record/<int:record_id>/',Update_record.as_view(),name='update-record'),
    path('delete-record/<int:record_id>/',Delete_record.as_view(),name='delete-record'),

    path('doctors/', Doctor_list.as_view(), name='doctors'),
    path('availability/',Slot_Available.as_view(), name='availability'),
    path('appointments/', Create_appointment.as_view(), name='appointments'),
    path('appointments/<int:pk>/reschedule/', Reschedule_appointment.as_view(), name='reschedule-appointment'),
    path('appointments/<int:pk>/cancel/', Cancel_appointment.as_view(), name='cancel-appointment'),


]


