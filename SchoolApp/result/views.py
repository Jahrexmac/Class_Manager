from django.shortcuts import render
from django.views.generic import ListView
from django.views import View
from .models import Classroom, Student, Subject
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

# Create your views here.
class Home(View):
    def get(self, request):
        return render(request, 'index.html')

class ClassListView(ListView):
    model = Classroom
    template_name = "classroom.html"

class StudentListView(View):

    def get(self, request, pk):
        std = Student.objects.filter(student_class=pk)
        try:
            std_class = std[0].student_class
        except IndexError:
            std = Classroom.objects.filter(pk = pk)
            std_class = std[0].name
            class_pk = std[0].pk
            return render(request, 'students.html', {'class': std_class, 'class_pk': class_pk})
        else:
            return render(request, 'students.html', {'students': std, 'class': std_class, 'pk': pk,})

class ClassCreateView(CreateView):
    model = Classroom
    template_name = "classroomnew.html"
    fields = ["name", "form_teacher"]

class StudentCreateView(CreateView):
    model = Student
    template_name = "studentnew.html"
    fields = ["student_class","first_name","last_name","middle_name","parent_name","parent_phone_number","house_address","religion"]

class ClassUpdate(UpdateView):
    model = Classroom
    template_name = 'editclassroom.html'
    fields = ['name', 'form_teacher']

class ClassDelete(DeleteView):
    model = Classroom
    template_name='deleteclassroom.html'
    success_url = reverse_lazy('class')

class StudentDetails(View):
    def get(self, request, pk):
        students = Student.objects.filter(pk = pk) # from data base
        subjects = Subject.objects.filter(student=pk) # from data base

        subjects = self.subject_process(subjects) # refine the subjects list of subject object to include total, grade and serial number
        
        totals = self.subject_total(subjects)
        #retrieve the class to get the pk so that the back key functionality would work for empty classes
        classroom = Classroom.objects.filter(name = students[0].student_class) 
        class_pk = classroom[0].pk

        std_name = students[0].first_name.title() + ' ' + students[0].last_name.title()
        pk = students[0].pk
        return render(request, 'studentdetails.html', {'students': students, 'name': std_name, 'pk': pk, 'class_pk': class_pk, 'subjects':subjects, 'totals': totals})
    
    def subject_process (self, subjects):
        """
            this function adds the serial number, total and grade to the subject object
        """
        subject_obj= []
        serial_num = 0
        for subject in subjects:
            serial_num += 1
            total = subject.first_test + subject.second_test + subject.exam
            grade = self.grade(total)
            subject.total = total
            subject.grade = grade
            subject.serial_number = serial_num
            subject_obj.append(subject)
        return subject_obj

    def subject_total(self, subjects):
        """
            Generate the grand total and average
        """
        grand_total = 0
        counter = 0
        check = False
        for subject in subjects:
            counter += 1
            grand_total += subject.total
        average = grand_total / counter
        average = f"{average:.2f}"

        if float(average) >= 60:
            check = True

        return {'average': float(average), 'grand_total': grand_total, 'check': check}

        # calculate grand total
        # calculate average
    def grade(self, total):
        """
        Returns the grade of each subjects
        """
        if total <= 39:
            return "F"
        elif total <= 49:
            return "P"
        elif total <= 59:
            return "C"
        elif total <= 69:
            return "B"
        elif total <= 79:
            return "B+"
        else:
            return "A"
        

class StudentUpdate(UpdateView):
    model = Student
    template_name = 'updatestudent.html'
    fields = ["student_class","first_name","last_name","middle_name","parent_name","parent_phone_number","house_address","religion"]

class StudentRemove(DeleteView):
    model = Student
    template_name='removestudent.html'
    success_url = reverse_lazy('class')

