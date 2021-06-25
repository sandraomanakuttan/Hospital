from django.urls import path
from . import views as user_views

urlpatterns = [
    path('',user_views.index,name='home'),
    path('contactus/',user_views.contactus,name='contactUs'),
    path('register/patient/',user_views.registerAsPatient,name='registerPatient'),
    path('register/doctor/',user_views.registerAsDoctor,name='registerDoctor'),
    path('login/',user_views.Login,name='login'),
    path('logout/',user_views.logout_view,name='Logout'),
    # path('patient/updateprofile2/',user_views.UpdateProfilePatient2,name='PatientUpdateProfile2'),
    path('patient/updateprofile/',user_views.UpdateProfilePatient,name='PatientUpdateProfile'),
    path('patient/<int:pk>/appointments/',user_views.AppointmentsPatient,name='PatientAppointments'),
    path('patient/<int:pk>/previoustreatments/',user_views.PreviousTreatmentsPatient,name='PatientPreviousTreatments'),
    path('patient/<int:pk>/invoicespayments/',user_views.InvoicesPaymentsPatient,name='PatientInvoicesPayments'),
    path('patient/<int:pk>/createappointments/',user_views.PatientCreateAppointment,name='PatientCreateAppointments'),

    path('doctor/updateprofile/',user_views.UpdateProfileDoctor,name='DoctorUpdateProfile'),
    path('doctor/<int:pk>/appointments/',user_views.AppointmentsDoctor,name='DoctorAppointments'),
    path('doctor/<int:pk>/previoustreatments/',user_views.PreviousTreatmentsDoctor,name='DoctorPreviousTreatments'),
    path('doctor/<int:pk>/createprescription/',user_views.CreatePrescriptionDoctor,name='DoctorCreatePerscription'),

    path('receiption/dashboard/',user_views.ReceiptionDashBoard,name='ReceiptionDashboard'),
    path('receiption/createappointment/',user_views.ReceiptionCreateAppointment,name='ReceiptionCreateAppointment'),
    path('receiption/<int:pk>/updateappointment/',user_views.ReceiptionUpdateAppointment,name='ReceiptionUpdateAppointment'),
    path('receiption/<int:pk>/updatepatient/',user_views.ReceiptionUpdateProfilePatient,name='ReceiptionUpdateProfilePatient'),
    path('receiption/<int:pk>/deletepatient/',user_views.ReceiptionDeleteProfilePatient,name='ReceiptionDeleteProfilePatient'),

    path('hr/dashboard/',user_views.HRDashboard,name='HRDashboard'),
    path('hr/dashboard/<int:pk>/updatedoctor/',user_views.HRUpdateDoctorProfile,name='HRUpdateDoctorProfile'),
    path('hr/accounting/',user_views.HRAccounting,name='HRAccounting'),
]