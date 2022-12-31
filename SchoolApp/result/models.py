from django.db import models
from django.urls import reverse

# Create your models here.
class Classroom(models.Model):
    name = models.CharField(max_length=10)
    form_teacher = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("class")
    

class Student(models.Model):
    student_class = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    first_name = models.CharField( max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    parent_name = models.CharField(max_length=50)
    parent_phone_number = models.CharField(max_length=11)
    house_address = models.CharField(max_length=200)
    religion = models.CharField(max_length=15)
    

    def __str__(self):
        return self.last_name + ' ' + self.first_name

    def get_absolute_url(self):
        return reverse("class")
    
class Subject(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    first_test = models.IntegerField()
    second_test = models.IntegerField()
    exam = models.IntegerField()

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("class")

    


