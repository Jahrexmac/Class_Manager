from django.contrib import admin
from .models import Student, Classroom, Subject

# Register your models here.
admin.site.register(Subject)
admin.site.register(Classroom)
admin.site.register(Student)