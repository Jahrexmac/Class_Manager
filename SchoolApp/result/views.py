from django.shortcuts import render
from django.views.generic import ListView
from django.views import View
from .models import Classroom, Student, Subject
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormMixin
from django.urls import reverse_lazy, reverse
from django import forms

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
    def post(self,request,pk):

        if 'save' in str(request.body):
            form = StudentNewForm(request.POST) #to save subject form
            if form.is_valid():
                form.save()

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

        if 'remove' in str(request.body):
            student = Student.objects.filter(pk = pk)

            classroom = Classroom.objects.filter(name = student[0].student_class)

            class_pk = classroom[0].pk
            std = Student.objects.filter(student_class=class_pk)

            Student.objects.filter(pk = pk ).delete() # deletes the student
            try:
                std_class = std[0].student_class
            except IndexError:
                std = Classroom.objects.filter(pk = pk)
                std_class = std[0].name
                class_pk = std[0].pk
                return render(request, 'students.html', {'class': std_class, 'class_pk': class_pk})
            else:
                return render(request, 'students.html', {'students': std, 'class': std_class, 'pk': pk,})
      
        if 'update' in str(request.body):
            print('yes')
            classroom = Classroom.objects.get(pk=pk)
            classroom.form_teacher = request.POST['form_teacher']
            classroom.name = request.POST['name']
            classroom.save()

            std = Student.objects.filter(student_class=pk)

            Student.objects.filter(pk = pk ).delete() # deletes the student
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
    #success_url = reverse_lazy('student', {'pk':self.object.pk})
    def get_success_url(self):
        return reverse('class')

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
    
    def post(self,request,pk):
        if 'save' in str(request.body):
            form = SubjectNewForm(request.POST) #to save subject form
            if form.is_valid():
                form.save()
            #print(pk)
            students = Student.objects.filter(pk=pk) # from data base
            subjects = Subject.objects.filter(student=pk) # from data base

            subjects = self.subject_process(subjects) # refine the subjects list of subject object to include total, grade and serial number
        
            totals = self.subject_total(subjects)
            #retrieve the class to get the pk so that the back key functionality would work for empty classes
            classroom = Classroom.objects.filter(name = students[0].student_class) 
            class_pk = classroom[0].pk

            std_name = students[0].first_name.title() + ' ' + students[0].last_name.title()
            pk = students[0].pk

            return render(request, 'studentdetails.html', {'students': students, 'name': std_name, 'pk': pk, 'class_pk': class_pk, 'subjects':subjects, 'totals': totals})
    
        if 'update' in str(request.body):
            subject = Subject.objects.get(pk=pk)
            subject.name = request.POST['name']
            subject.first_test = request.POST['first_test']
            subject.second_test = request.POST['second_test']
            subject.exam = request.POST['exam']
            subject.save()

            students = Student.objects.filter(subject=pk) # from data base
            student_pk = students[0].pk
            subjects = Subject.objects.filter(student=student_pk) # from data base

            subjects = self.subject_process(subjects) # refine the subjects list of subject object to include total, grade and serial number
        
            totals = self.subject_total(subjects)
            #retrieve the class to get the pk so that the back key functionality would work for empty classes
            classroom = Classroom.objects.filter(name = students[0].student_class) 
            class_pk = classroom[0].pk

            std_name = students[0].first_name.title() + ' ' + students[0].last_name.title()
            pk = students[0].pk

            return render(request, 'studentdetails.html', {'students': students, 'name': std_name, 'pk': pk, 'class_pk': class_pk, 'subjects':subjects, 'totals': totals})
        if 'changes' in str(request.body):
            
            student = Student.objects.get(pk=pk)
            student.first_name = request.POST['first_name']
            student.last_name = request.POST['last_name']
            student.middle_name = request.POST['middle_name']
            student.parent_name =request.POST['parent_name']
            student.parent_phone_number = request.POST['parent_phone_number']
            student.house_address = request.POST['house_address']
            student.religion = request.POST['religion']
            student.save()

            students = Student.objects.filter(pk=pk) # from data base
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
        if grand_total > 0 :
            average = grand_total / counter
        else:
            average = 0.00
    
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
        
class SubjectNewForm(forms.ModelForm):
    class Meta:
        model= Subject
        fields = ["student","name", "first_test", "second_test", "exam"]

class StudentNewForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["student_class","first_name","last_name","middle_name","parent_name","parent_phone_number","house_address","religion"]

        
class StudentUpdate(UpdateView):
    model = Student
    template_name = 'updatestudent.html'
    fields = ["student_class","first_name","last_name","middle_name","parent_name","parent_phone_number","house_address","religion"]

class StudentRemove(DeleteView):
    model = Student
    template_name='removestudent.html'
    success_url = reverse_lazy('class')

class SubjectNew(CreateView):
    model = Subject
    template_name = "subjectnew.html"
    fields = ["student","name", "first_test", "second_test", "exam"]

class SubjectUpdate(UpdateView):
    model = Subject
    template_name = "subjectupdate.html"
    fields = ["name", "first_test", "second_test", "exam"]
