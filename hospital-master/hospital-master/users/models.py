from django.db import models


from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from users.countries import COUNTRIES

class User(AbstractUser):
    is_Patient=models.BooleanField('Patient Status',default=False)
    is_Doctor=models.BooleanField('Doctor Status',default=False)
    is_Receptionist=models.BooleanField('Receptionist Status',default=False)
    is_hr = models.BooleanField('HR Status',default=False)

class Patient(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    age = models.IntegerField(null=True)

    GENDER=(
        ("Male","Male"),
        ("Female","Female"),
    )
    gender = models.CharField(choices=GENDER,null=True, max_length = 10)
    phone_no = PhoneNumberField()
    BLOOD_GROUP = (
        ('A+','A+'),
        ('A-','A-'),
        ('B+','B+'),
        ('B-','B-'),
        ('AB+','AB+'),
        ('AB-','AB-'),
        ('O+','O+'),
        ('O-','O-'),
        ('bombay', 'Bombay'),
    )
    bloodgroup = models.CharField(max_length=15,null=True,choices=BLOOD_GROUP)

    street_Line_1 = models.CharField(null=True,max_length=35)
    street_Line_2 = models.CharField(null=True,max_length=35)
    city = models.CharField(null=True,max_length=35)
    state = models.CharField(null=True,max_length=35)
    country = models.CharField(null=True,max_length=35,choices = COUNTRIES)
    zipcode = models.CharField(null=True,max_length=10)

    def __str__(self):
        return self.user.first_name+" "+ self.user.last_name
    

class Departments(models.Model):
    department_name = models.CharField(max_length=35,null=False)

    def __str__(self):
        return self.department_name

class Doctor(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    age = models.IntegerField(null=True)

    GENDER = (
        ("Male","Male"),
        ("Female","Female"),
    )
    gender = models.CharField(choices=GENDER,null=True,max_length=12)
    phone_no = PhoneNumberField()
    BLOOD_GROUP = (
        ('A+','A+'),
        ('A-','A-'),
        ('B+','B+'),
        ('B-','B-'),
        ('AB+','AB+'),
        ('AB-','AB-'),
        ('O+','O+'),
        ('O-','O-'),
        ('bombay', 'Bombay'),
    )
    bloodgroup = models.CharField(max_length=15,null=True,choices=BLOOD_GROUP)

    street_Line_1 = models.CharField(null=True,max_length=25)
    street_Line_2 = models.CharField(null=True,max_length=25)
    city = models.CharField(null=True,max_length=30)
    state = models.CharField(null=True,max_length=35)
    country = models.CharField(null=True,max_length=25,choices = COUNTRIES)
    zipcode = models.CharField(null=True,max_length=10)

    department = models.ForeignKey(Departments,on_delete=models.CASCADE)
    salary = models.IntegerField(default=0)
    attendance = models.IntegerField(default=0)

    STATUS = (
        ('Active','Active'),
        ('Inactive','Inactive'),
    )
    status = models.CharField(max_length = 15, choices = STATUS,default = 'Inactive')

    def __str__(self):
        return self.user.first_name+" "+ self.user.last_name

class Receiptionist(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)

class HumanResource(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)

class Appointments(models.Model):
    date = models.DateField(null=False)
    time = models.TimeField(null=False)
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor,on_delete=models.CASCADE)

    STATUS = (
        ('Confirmed','Confirmed'),
        ('Pending','Pending'),
        ('Cancelled','Cancelled'),
        ('Completed','Completed'),
    )

    status = models.CharField(max_length=20,choices=STATUS,default='Pending')
    paid = models.IntegerField(default=0,null=True)
    outstanding = models.IntegerField(default=0,null=True)
    total = models.IntegerField(default=0,null = True)

class Prescription(models.Model):
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    doctor = models.ForeignKey(Doctor,on_delete=models.CASCADE)
    symptoms = models.CharField(max_length=70)
    prescription = models.TextField()
