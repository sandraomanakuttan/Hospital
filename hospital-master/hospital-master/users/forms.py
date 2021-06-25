from django import forms
from .models import Patient,User,Doctor,Appointments, Prescription

class LoginForm(forms.Form):
    username = forms.CharField(label="Username", required=True)
    password = forms.CharField(label="Password",max_length=32, widget=forms.PasswordInput)


class UserForm(forms.Form):
    username = forms.CharField(label='Username',required=True)
    first_name = forms.CharField(label='First Name',required=True)
    last_name = forms.CharField(label='Last Name',required=True)
    email = forms.EmailField(label='Email', required= True)
    password = forms.CharField(label="Password",max_length=32, widget=forms.PasswordInput)

class PatientRegistrationForm(forms.ModelForm):

    class Meta:
        model = Patient
        fields = ['age', 'street_Line_1', 'street_Line_2', 'city','state', 'phone_no','zipcode','bloodgroup','country','gender']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email']

class PatientUpdateForm(forms.Form):
    first_name = forms.CharField(max_length=25,required = True)
    last_name = forms.CharField(max_length=25,required = True)
    email = forms.EmailField(required = True)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=32, widget=forms.PasswordInput)

    address_line_1 = forms.CharField(max_length=30,required = True)
    address_line_2 = forms.CharField(max_length=30)
    city = forms.CharField(max_length=35,required = True)
    state = forms.CharField(max_length=35,required = True)
    zipcode = forms.CharField(max_length=15)
    country = forms.CharField(label = 'Country', max_length=35)

    mobile = forms.CharField(max_length=15,required = True)
    gender = forms.ChoiceField(label="gender",choices=Patient.GENDER,widget=forms.RadioSelect)
    age = forms.IntegerField(min_value=0,max_value=150,required = True)
    bloodgroup = forms.CharField(max_length=5,required = True,widget=forms.Select(choices=Patient.BLOOD_GROUP))

class DoctorUpdateForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['age', 'street_Line_1', 'street_Line_2', 'city','state', 'phone_no','zipcode','bloodgroup','department','gender','country']

class DoctorUpdateFormForHR(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['age', 'street_Line_1', 'street_Line_2', 'city','state', 'phone_no','zipcode','bloodgroup', 'status','salary','attendance','department','gender','country']

class TimeInput(forms.TimeInput):
    input_type = "time"

    def __init__(self, **kwargs):
        kwargs["format"] = "%H:%M %p"
        super().__init__(**kwargs)

class DateInput(forms.DateInput):
    input_type = "date"

    def __init__(self, **kwargs):
        kwargs["format"] = "%m/%d/%Y"
        super().__init__(**kwargs)

class CreateAppointmentReceiption(forms.ModelForm):

    class Meta:
        model = Appointments
        fields = ['date','time','patient','doctor','status','paid','total','outstanding']
        widgets= {
            'date' : DateInput(),
        }
    # def __init__(self, *args, **kwargs):
    #     self.fields['time'].widget = forms.SelectDateWidget()

class CreatePrescriptionDoctorForm(forms.ModelForm):

    class Meta:
        model = Prescription
        fields = ['doctor','patient','symptoms','prescription']
        widgets ={
            'prescription' : forms.Textarea(),
        }

class CreateAppointmentPatient(forms.ModelForm):
    
    class Meta:
        model = Appointments
        fields = ['date','time','patient','doctor']
        widgets= {
            'date' : DateInput(),
        }