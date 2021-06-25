from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .forms import LoginForm, PatientRegistrationForm, PatientUpdateForm, UserForm, DoctorUpdateForm, DoctorUpdateFormForHR,CreateAppointmentReceiption, CreatePrescriptionDoctorForm, CreateAppointmentPatient
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from .models import User,Patient,Doctor,Departments,Appointments
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.forms.models import model_to_dict
from django.contrib import messages
from django.db.models import Sum

# Create your views here.
def Patient_Required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and u.is_active and u.is_Patient,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def Doctor_Required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and u.is_active and u.is_Doctor,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def Receiptionist_Required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and u.is_active and u.is_Receptionist,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def HR_Required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and u.is_active and u.is_hr,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def index(request):
    return render(request,'users/index.html')

def contactus(request):
    return render(request,'users/ContactUs.html')

def registerAsPatient(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('names[first_name]')
        last_name = request.POST.get('names[last_name]')
        password1 = request.POST.get('password_1')
        password2 = request.POST.get('password')

        if password1 != password2:
            return render(request,'users/RegisterAsPatient.html')
        password = make_password(password1)

        mobile = request.POST.get('mobile')
        age = request.POST.get('age')
        address_line_1 = request.POST.get('address_1[address_line_1]')
        address_line_2 = request.POST.get('address_1[address_line_2]')
        city = request.POST.get('address_1[city]')
        state = request.POST.get('address_1[state]')
        zipcode = request.POST.get('address_1[zip]')
        country = request.POST.get('address_1[country]')
        gender = request.POST.get('gender')
        bloodGroup = request.POST.get('bloodgroup')

        user = User(username=username,password=password,email=email,first_name=first_name,last_name=last_name,is_Patient=True)
        user.save()
        patient = Patient(
            user=user,
            age = age,
            gender = gender,
            phone_no = mobile,
            bloodgroup = bloodGroup,
            street_Line_1 = address_line_1,
            street_Line_2 = address_line_2,
            city = city,
            state = state,
            country = country,
            zipcode = zipcode
        )
        patient.save()
        return redirect('/login')

    return render(request,'users/RegisterAsPatient.html')

def registerAsDoctor(request):

    if request.method == 'POST':
        print(request.POST)
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('names[first_name]')
        last_name = request.POST.get('names[last_name]')
        password1 = request.POST.get('password_1')
        password2 = request.POST.get('password')

        if password1 != password2:
            return render(request,'users/RegisterAsPatient.html')
        password = make_password(password1)

        mobile = request.POST.get('mobile')
        age = request.POST.get('age')
        address_line_1 = request.POST.get('address_1[address_line_1]')
        address_line_2 = request.POST.get('address_1[address_line_2]')
        city = request.POST.get('address_1[city]')
        state = request.POST.get('address_1[state]')
        zipcode = request.POST.get('address_1[zip]')
        country = request.POST.get('address_1[country]')
        gender = request.POST.get('gender')
        bloodGroup = request.POST.get('bloodgroup')
        department_name = request.POST.get('department')
        department = Departments.objects.filter(department_name=department_name)
        if department is not None:
            department = department[0]
        else:
            department = Departments.objects.all()[0]

        user = User(username=username,password=password,email=email,first_name=first_name,last_name = last_name,is_Doctor = True)
        user.save()
        doctor = Doctor(
            user=user,
            age = age,
            gender = gender,
            phone_no = mobile,
            bloodgroup = bloodGroup,
            street_Line_1 = address_line_1,
            street_Line_2 = address_line_2,
            city = city,
            state = state,
            country = country,
            zipcode = zipcode,
            department = department
        )
        doctor.save()
        return redirect('/login')

    return render(request,'users/RegisterAsDoctor.html')

def Login(request):

    if request.method == 'POST':
        loginForm = LoginForm(request.POST)
        print(request.POST)

        if loginForm.is_valid():
            username = loginForm.cleaned_data['username']
            password = loginForm.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                context = {
                    'loginform' : loginForm
                }
                return render(request,'users/Login.html',context=context)

        else:
            # print(loginForm.username)
            context={
                'loginform' : loginForm,
            }
            return render(request,'users/Login.html',context=context)

    return render(request,'users/Login.html')

def logout_view(request):
    logout(request)
    return redirect('/')

@Patient_Required
def UpdateProfilePatient(request):

    if request.method == 'POST':
        userform = UserForm(request.POST,instance=request.user)
        patientform = PatientRegistrationForm(request.POST,instance=request.user.patient)

        if userform.is_valid() and patientform.is_valid():
            userform.save()
            patientform.save()
            messages.success(request,f'Profile Successfully Updated!')
            return render(request,'users/index.html')
        else:
            context = {
                'u_form' : userform,
                'p_form' : patientform,
            }
            return render(request,'users/EditPatientProfile.html',context=context)
    else:
        userform = UserForm(instance=request.user)
        patientform = PatientRegistrationForm(instance=request.user.patient)
        
        context = {
            'u_form' : userform,
            'p_form' : patientform,
        }
        return render(request,'users/EditPatientProfile.html',context=context)

@Patient_Required
def AppointmentsPatient(request,pk):
    patient = Patient.objects.filter(pk=pk)
    appointments = None
    if len(patient)>0:
        appointments = patient[0].appointments_set.all()
        if len(appointments)<=0:
            appointments = None

    context ={
        'patient': patient[0],
        'appointments' : appointments,
    }

    return render(request,'users/YourAppointmentsPatients.html',context=context)

@Patient_Required
def PreviousTreatmentsPatient(request,pk):
    patient = Patient.objects.filter(pk=pk)
    prescriptions = None
    if len(patient)>0:
        prescriptions = patient[0].prescription_set.all().order_by('-date').order_by('-time')
        if len(prescriptions)<=0:
            prescriptions = None

    context = {
        'patient' : patient[0],
        'prescriptions' : prescriptions,
    }
    return render(request,'users/PreviousMedicalTreatmentPatient.html',context=context)

@Patient_Required
def InvoicesPaymentsPatient(request,pk):

    patient = Patient.objects.filter(pk=pk)[0]
    appointments = None
    if patient:
        appointments = Appointments.objects.filter(patient=patient)
    
    context = {
        'patient' : patient,
        'appointments' : appointments,
    }

    return render(request,'users/InvoicesAndPayments.html',context=context)

@Patient_Required
def PatientCreateAppointment(request,pk):

    doctors = Doctor.objects.all()
    patient = Patient.objects.filter(pk=pk)[0]

    if request.method == 'POST':
        appointmentform = CreateAppointmentPatient(request.POST)
        print(request.POST)
        if appointmentform.is_valid():
            appointmentform.save()
            messages.success(request,f'Profile Successfully Updated!')
            return redirect('home')
        else:
            print(appointmentform.is_valid())
            context = {
                'form' : appointmentform,
            }
            return render(request,'users/CreateAppointmentPatient.html',context=context)
    else:
        appointmentform = CreateAppointmentReceiption()

        context ={
            'form' : appointmentform,
        }

        return render(request,'users/CreateAppointmentPatient.html',context=context)


@Doctor_Required
def UpdateProfileDoctor(request):

    if request.method == 'POST':
        # print(request.POST)
        userform = UserForm(request.POST,instance=request.user)
        doctorform = DoctorUpdateForm(request.POST,instance=request.user.doctor)

        if userform.is_valid() and doctorform.is_valid():
            userform.save()
            doctorform.save()
            messages.success(request,f'Profile Successfully Updated!')
            return render(request,'users/index.html')
        else:
            context = {
                'u_form' : userform,
                'p_form' : doctorform,
            }
            return render(request,'users/UpdateDoctorProfile.html',context=context)
    else:
        userform = UserForm(instance=request.user)
        doctorform = DoctorUpdateForm(instance=request.user.doctor)
        print(doctorform.is_valid(),userform.is_valid())
        context = {
            'u_form' : userform,
            'p_form' : doctorform,
        }
        return render(request,'users/UpdateDoctorProfile.html',context=context)

    return render(request,'users/UpdateDoctorProfile.html')

@Doctor_Required
def AppointmentsDoctor(request,pk):
    doctor = get_object_or_404(Doctor,pk=pk)
    appointments = doctor.appointments_set.all()
    if len(appointments)<=0:
        appointments = None
    context ={
        'doctor': doctor,
        'appointments' : appointments,
    }
    return render(request,'users/YourAppointmentsDoctor.html',context=context)

@Doctor_Required
def PreviousTreatmentsDoctor(request,pk):
    doctor = get_object_or_404(Doctor,pk=pk)
    prescriptions = doctor.prescription_set.all().order_by('-date').order_by('-time')
    if len(prescriptions)<=0:
        prescriptions = None
    context = {
        'doctor' : doctor,
        'prescriptions' : prescriptions,
    }
    
    return render(request,'users/PreviousMedicalTreatmentDoctor.html',context=context)

@Doctor_Required
def CreatePrescriptionDoctor(request,pk):

    if request.method == 'POST':
        doctor = Doctor.objects.filter(pk=pk)[0]
        prescriptionform = CreatePrescriptionDoctorForm(request.POST,initial={'doctor':doctor})

        if prescriptionform.is_valid():
            prescriptionform.save()
            return redirect('DoctorPreviousTreatments',pk=pk)

        else:
            doctor = Doctor.objects.filter(pk=pk)[0]
            prescriptionform = CreatePrescriptionDoctorForm(request.POST,initial={'doctor':doctor})

            context = {
                'doctor' : doctor,
                'form' : prescriptionform,
            }
            return render(request,'users/CreatePrescriptionDoctor.html',context=context)
    else:
        doctor = Doctor.objects.filter(pk=pk)[0]
        prescriptionform = CreatePrescriptionDoctorForm(initial={'doctor':doctor})

        context = {
            'doctor' : doctor,
            'form' : prescriptionform,
        }
        return render(request,'users/CreatePrescriptionDoctor.html',context=context)
    

@Receiptionist_Required
def ReceiptionDashBoard(request):
    appointments = Appointments.objects.all().order_by('-date').order_by('-time')
    patients = Patient.objects.all()
    appcnt = Appointments.objects.count()
    appupcome = Appointments.objects.filter(status='Pending').count()
    appdone = Appointments.objects.filter(status='Completed').count()

    context = {
        'appointments' : appointments,
        'patients' : patients,
        'appcnt' : appcnt,
        'appupcome' : appupcome,
        'appdone' : appdone,
    }
    return render(request,'users/ReceiptionDashboard.html',context=context)

@Receiptionist_Required
def ReceiptionCreateAppointment(request):

    doctors = Doctor.objects.all()
    patient = Patient.objects.all()

    if request.method == 'POST':
        appointmentform = CreateAppointmentReceiption(request.POST)
        print(request.POST)
        if appointmentform.is_valid():
            appointmentform.save()
            messages.success(request,f'Profile Successfully Updated!')
            return redirect('home')
        else:
            print(appointmentform.is_valid())
            context = {
                'form' : appointmentform,
            }
            return render(request,'users/CreateAppointmentforPatient.html',context=context)
    else:
        appointmentform = CreateAppointmentReceiption()

        context ={
            'form' : appointmentform,
        }

        return render(request,'users/CreateAppointmentforPatient.html',context=context)


@Receiptionist_Required
def ReceiptionUpdateAppointment(request,pk):

    if request.method == 'POST':
        appointment = Appointments.objects.filter(pk=pk)[0]
        appointmentform = CreateAppointmentReceiption(request.POST)
        print(request.POST)
        if appointmentform.is_valid():
            appointmentform.save()
            messages.success(request,f'Profile Successfully Updated!')
            return redirect('home')
        else:
            print(appointmentform.is_valid())
            context = {
                'form' : appointmentform,
            }
            return render(request,'users/UpdateAppointmentReceiption.html',context=context)
    else:
        appointment = Appointments.objects.filter(pk=pk)[0]
        appointmentform = CreateAppointmentReceiption(instance=appointment)

        context ={
            'form' : appointmentform,
        }

        return render(request,'users/UpdateAppointmentReceiption.html',context=context)


@Receiptionist_Required
def ReceiptionUpdateProfilePatient(request,pk):

    if request.method == 'POST':
        patient = Patient.objects.filter(pk=pk)[0]
        userform = UserForm(request.POST,instance=patient.user)
        patientform = PatientRegistrationForm(request.POST,instance=patient)

        if userform.is_valid() and patientform.is_valid():
            userform.save()
            patientform.save()
            messages.success(request,f'Profile Successfully Updated!')
            return render(request,'users/index.html')
        else:
            context = {
                'u_form' : userform,
                'p_form' : patientform,
                'patient' : patient,
            }
            return render(request,'users/UpdatePatientProfileReceiption.html',context=context)
    else:
        patient = Patient.objects.filter(pk=pk)[0]
        userform = UserForm(instance=patient.user)
        patientform = PatientRegistrationForm(instance=patient)
        
        context = {
            'u_form' : userform,
            'p_form' : patientform,
            'patient' : patient,
        }
        return render(request,'users/UpdatePatientProfileReceiption.html',context=context)

@Receiptionist_Required
def ReceiptionDeleteProfilePatient(request,pk):

    if request.method == 'POST':
        if request.POST.get('delete'):
            User.objects.filter(pk=pk)[0].delete()
            return redirect('ReceiptionDashboard')

    else:
        patient = Patient.objects.filter(pk=pk)[0]
        context ={
            'patient' : patient,
        }
        return render(request,'users/DeletePatient.html',context)

    return render(request,'users/DeletePatient.html',context=context)

@HR_Required
def HRDashboard(request):

    doctors = Doctor.objects.all()
    doctorsact = Doctor.objects.filter(status="Active")
    patcnt = Patient.objects.count()
    if len(doctors)<=0:
        doctors = None
    context = {
        'doctors' : doctors,
        'totaldoctors' : len(doctors),
        'actdoctors' : len(doctorsact),
        'noofpatients' : patcnt,
    }

    return render(request,'users/HRDashboard.html', context=context)

@HR_Required
def HRUpdateDoctorProfile(request,pk):

    if request.method == 'POST':
        # print(request.POST)
        doctor = Doctor.objects.filter(pk=pk)[0]
        userform = UserForm(request.POST,instance=doctor.user)
        doctorform = DoctorUpdateFormForHR(request.POST,instance=doctor)

        if userform.is_valid() and doctorform.is_valid():
            userform.save()
            doctorform.save()
            messages.success(request,f'Profile Successfully Updated!')
            return redirect('HRDashboard')
        else:
            context = {
                'u_form' : userform,
                'p_form' : doctorform,
            }
            return render(request,'users/UpdateDoctorProfileForHR.html',context=context)
    else:
        doctor = Doctor.objects.filter(pk=pk)[0]
        userform = UserForm(instance=doctor.user)
        doctorform = DoctorUpdateFormForHR(instance=doctor)
        print(doctorform.is_valid(),userform.is_valid())
        context = {
            'u_form' : userform,
            'p_form' : doctorform,
            'doctor' :doctor,
        }
        return render(request,'users/UpdateDoctorProfileForHR.html',context=context)

    return render(request,'users/UpdateDoctorProfileForHR.html')

@HR_Required
def HRAccounting(request):

    appointments = Appointments.objects.all()
    if len(appointments)<=0:
        appointments = None
    
    # patients = Patient.objects.all()
    # if len(patients)<=0:
    #     patients = None
    
    # if patients:
    #     PatientAppointments = []
    #     for patient in patients:
    #         appointmentPatient = Appointments.objects.filter(patient=patient)
    #         if len(appointmentPatient)<=0:
    patientsAppointPaid = Appointments.objects.values('patient').annotate(Sum('paid'))
    patientsAppointOutstanding = Appointments.objects.values('patient').annotate(Sum('outstanding'))
    patientsPaid = []
    for i in patientsAppointPaid:
        patientsPaid.append(Patient.objects.filter(pk=i['patient'])[0])

    listreq = []
    for i in range(len(patientsPaid)):
        listreq.append((patientsPaid[i],patientsAppointOutstanding[i],patientsAppointPaid[i]))
    
    if len(listreq)<=0:
        listreq = None

    context = {
        'appointments' : appointments,
        'patientsAppointPaid' : patientsAppointPaid,
        'patientsPaid' : patientsPaid,
        'patientsAppointOutstanding' : patientsAppointOutstanding,
        'listreq' : listreq
    }

    return render(request,'users/Accounting.html',context=context)