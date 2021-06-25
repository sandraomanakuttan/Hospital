from django.contrib import admin

# Register your models here.
from .models import *
from django.contrib.auth.admin import UserAdmin

admin.site.register(User,UserAdmin)
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Receiptionist)
admin.site.register(HumanResource)
admin.site.register(Departments)
admin.site.register(Appointments)
admin.site.register(Prescription)