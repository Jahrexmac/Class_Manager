
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views import View
from .models import Classroom, Student, Subject
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormMixin
from django.urls import reverse_lazy, reverse
from django import forms
import io
from django.http import FileResponse
from utilities.result_generator import generate_result_pdf
from utilities.subject_processor import result_display
import os
from .forms import SignupForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
#from django.contrib.auth.models import User
from django.contrib.auth import logout


#back functionality variable for the add student html template
global_class_pk = 0
global_student_pk = 0

# Create your views here.


#-------------------------------------------RESULT GENERATORS VIEWS-------------------------------------------------

class Results(View):
    @method_decorator(login_required(login_url='index'))
    def get(self, request, pk):
        '''
    1. retreive all students
    2. get thier pk 
    3. use pk to retreive all subject and store all in a new a array
    4.process the result
    
    '''
        classroom = Classroom.objects.filter(pk = pk)
        class_pk = classroom[0].pk
        students = Student.objects.filter(student_class = class_pk) # from data base
        student_pk = students[0].pk
        sub = 'subject placeholder'

        class_result = result_display(students,sub,student_pk,checker= False)
        '''
            the result contain 
            1. object of results
            2. object single student
            3. list of subjects
        '''
        #subjects = self.subject_process(subjects) # refine the subjects list of subject object to include total, grade and serial number
        #return students, std_name, pk, class_pk, subjects and totals
        return render(request, 'results.html', {'class_result': class_result, 'class_pk': class_pk})


#pdf implement
class ResultPdf(View):
    @method_decorator(login_required(login_url='index'))
    def get(self, request, pk):

        
        '''
    1. retreive all students
    2. get thier pk 
    3. use pk to retreive all subject and store all in a new a array
    4.process the result
    
    '''
        classroom = Classroom.objects.filter(pk = pk)
        class_pk = classroom[0].pk
        students = Student.objects.filter(student_class = class_pk) # from data base
        student_pk = students[0].pk
        sub = 'subject placeholder'

        class_result = result_display(students,sub,student_pk,checker= False)
        '''
            the result contain 
            1. object of results
            2. object single student
            3. list of subjects
        '''
        #subjects = self.subject_process(subjects) # refine the subjects list of subject object to include total, grade and serial number
        #return students, std_name, pk, class_pk, subjects and totals
        #print(class_result)
        buffer = generate_result_pdf(class_result)
        if class_result:
            return FileResponse(buffer, as_attachment=False,filename=f'{class_result[0]["student_class"]}_results.pdf')
        else:
            return FileResponse(buffer, as_attachment=False,filename='No_result.pdf')

#end pdf implement





class StudentListView(View):
    @method_decorator(login_required(login_url='index'))
    def get(self, request, pk):
        num_students = 0
        if global_class_pk:
            if pk:
                std = Student.objects.filter(student_class= pk) 
            if not std:
                std = Student.objects.filter(student_class= global_class_pk)
            try:
                std_class = std[0].student_class
                class_pk = std[0].student_class_id
                num_students = len(std)
            except IndexError:
                cls = Classroom.objects.filter(pk = pk)
                std_class = cls[0].name
                class_pk = cls[0].pk
                num_students = 0
                return render(request, 'students.html', {'class': std_class, 'class_pk': class_pk, 'num_students': num_students})
            else:
                return render(request, 'students.html', {'students': std, 'class': std_class, 'pk': class_pk, 'class_pk': class_pk, 'num_students': num_students})
        else:
            std = Student.objects.filter(student_class= pk)
            try:
                std_class = std[0].student_class
                class_pk = std[0].student_class_id
                num_students = len(std)
            except IndexError:
                cls = Classroom.objects.filter(pk = pk)
                std_class = cls[0].name
                class_pk = cls[0].pk
                num_students = 0
                return render(request, 'students.html', {'class': std_class, 'class_pk': class_pk, 'num_students': num_students})
            else:
                return render(request, 'students.html', {'students': std, 'class': std_class, 'pk': class_pk, 'class_pk': class_pk, 'num_students': num_students}) 

    @method_decorator(login_required(login_url='index'))
    def post(self,request,pk):
        num_students = 0
        if 'save' in request.POST:
            form = StudentNewForm(request.POST, request.FILES) #to save subject form
            if form.is_valid():
                form.save()

            last_student = Student.objects.last() # retrieve the last student
            std = Student.objects.filter(student_class=last_student.student_class_id)
            num_students = len(std)
            
            std_class = std[0].student_class
            pk = last_student.student_class_id
            return render(request, 'students.html', {'students': std, 'class': std_class, 'pk': pk, 'class_pk': pk, 'num_students': num_students})

        if 'remove' in str(request.body):
            student = Student.objects.filter(pk = pk)
            classroom = Classroom.objects.filter(name = student[0].student_class)
            std_class = classroom[0].name
            class_pk = classroom[0].pk

            global global_class_pk  # Edit the global class pk
            global_class_pk = class_pk

            std = Student.objects.filter(student_class=class_pk)

            Student.objects.filter(pk = pk ).delete() # deletes the student
            try:
                #class_pk = std[0].student_class
                num_students = len(std)
            except IndexError:
                num_students = 0
                classroom = Classroom.objects.filter(pk = class_pk)
                std_class = classroom[0].name
                class_pk = classroom[0].pk
                return render(request, 'students.html', {'class': std_class, 'class_pk': class_pk, 'num_students': num_students})
            else:
                return render(request, 'students.html', {'students': std, 'class': std_class, 'pk': class_pk, 'class_pk': class_pk, 'num_students': num_students})
      
        if 'update' in str(request.body):
            
            classroom = Classroom.objects.get(pk=pk)
            classroom.form_teacher = request.POST['form_teacher']
            classroom.name = request.POST['name']
            classroom.save()

            std = Student.objects.filter(student_class=pk)

            #Student.objects.filter(pk = pk ).delete() # deletes the student
            try:
                std_class = std[0].student_class
                num_students = len(std)
            except IndexError:
                num_students = 0
                std = Classroom.objects.filter(pk = pk)
                std_class = std[0].name
                class_pk = std[0].pk
                return render(request, 'students.html', {'class': std_class, 'class_pk': class_pk, 'num_students': num_students})
            else:
                return render(request, 'students.html', {'students': std, 'class': std_class, 'pk': pk, 'class_pk': pk, 'num_students': num_students})
      
class StudentDetails(View):
    @method_decorator(login_required(login_url='index'))
    def get(self, request, pk):

        if global_student_pk:
            if pk:
                students = Student.objects.filter(pk = pk) # from data base
                subjects = Subject.objects.filter(student=pk) # from data base
            if not students: #check if students object is empty
                students = Student.objects.filter(pk = global_student_pk) # from data base
                subjects = Subject.objects.filter(student= global_student_pk) # from data base
                pk = global_student_pk

        #subjects = self.subject_process(subjects) # refine the subjects list of subject object to include total, grade and serial number
        #return students, std_name, pk, class_pk, subjects and totals
            return render(request, 'studentdetails.html', result_display(students,subjects,pk, checker=True))
        else:
            students = Student.objects.filter(pk = pk) # from data base
            subjects = Subject.objects.filter(student=pk) # from data base
            return render(request, 'studentdetails.html', result_display(students,subjects,pk, checker=True))
    
    @method_decorator(login_required(login_url='index'))
    def post(self,request,pk):
        if 'save' in request.POST:
            form = SubjectNewForm(request.POST) #to save subject form
            if form.is_valid():
                form.save()
            
            subject = Subject.objects.last() # retrieve last object from the data base

            students = Student.objects.filter(pk= subject.student_id) # from data base
            subjects = Subject.objects.filter(student= subject.student_id) # from data base

            return render(request, 'studentdetails.html',result_display(students,subjects,subject.student_id, checker=True))
            
        if 'update' in request.POST:
            subject = Subject.objects.get(pk=pk)
            subject.name = request.POST['name']
            subject.first_test = request.POST['first_test']
            subject.second_test = request.POST['second_test']
            subject.exam = request.POST['exam']
            subject.save()

            students = Student.objects.filter(subject=pk) # from data base
            student_pk = students[0].pk

            global global_student_pk # back functionality for subject update view
            global_student_pk = student_pk

            subjects = Subject.objects.filter(student=student_pk) # from data base

            return render(request, 'studentdetails.html', result_display(students,subjects, student_pk, checker=True))

        
        if 'changes' in request.POST:
            
            student = Student.objects.get(pk=pk)
            image_path = student.profile_picture.path

            form = StudentNewForm(request.POST, request.FILES,instance=student) #to save subject form
        
            if form.is_valid():
                if os.path.exists(image_path):
                    os.remove(image_path)
                form.save()
            else:
                print('not valid')
                print(form.errors)

            students = Student.objects.filter(pk=pk) # from data base
            subjects = Subject.objects.filter(student=pk) # from data base
            
            return render(request, 'studentdetails.html',result_display(students,subjects,pk, checker=True))
              
        if 'delete' in request.POST:
            subject = Subject.objects.filter(pk = pk)
            
            student_pk = subject[0].student_id

            # back functionality for subject update view
            global_student_pk = student_pk

            students = Student.objects.filter(pk = student_pk)
            subjects = Subject.objects.filter(student = student_pk) # from data base

            Subject.objects.filter(pk = pk ).delete() # deletes the student
            
            return render(request, 'studentdetails.html', result_display(students,subjects,student_pk, checker=True))


class Home(View):
    
    def post(self, request):
        return render(request, 'home.html')

    @method_decorator(login_required(login_url='index'))
    def get(self,request):
        return render(request, 'home.html')
class Index(View):
    
    def get(self, request):
        return render(request, 'index.html')

class ClassListView(View):
    @method_decorator(login_required(login_url='index'))
    def get(self, request):
        classroom = Classroom.objects.filter(user = request.user) # from data base
        return render(request,"classroom.html",{'classroom_list': classroom})



#-----------------------------------------------STUDENTS VIEWS-------------------------------------------------
class StudentNewForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        #["student_class","profile_picture","first_name","last_name","middle_name","parent_name","parent_phone_number","house_address","religion"]

class StudentCreateView(CreateView):
    
    model = Student
    template_name = "studentnew.html"
    fields = ["student_class","profile_picture", "first_name","last_name","middle_name","parent_name","parent_phone_number","house_address","religion"]

# Field limiting to current class
    def get_form_class(self):
        path = self.request.get_full_path()
        class_list = path.split('/') 
        class_pk = int(class_list[-1])
        modelform = super().get_form_class()
        modelform.base_fields['student_class'].limit_choices_to = {'pk': class_pk}
        return modelform

class StudentUpdate(UpdateView):
    model = Student
    template_name = 'updatestudent.html'
    fields = '__all__'
    #["profile_picture","first_name","last_name","middle_name","parent_name","parent_phone_number","house_address","religion"]
#"student_class",
class StudentRemove(DeleteView):
    model = Student
    template_name='removestudent.html'
    success_url = reverse_lazy('class')


#-----------------------------------------------SUBJECT VIEWS-------------------------------------------------
class SubjectNewForm(forms.ModelForm):
    class Meta:
        model= Subject
        fields = ["student","name", "first_test", "second_test", "exam"]
class SubjectNew(CreateView):
    model = Subject
    template_name = "subjectnew.html"
    fields = ["student","name", "first_test", "second_test", "exam"]

#  To limit the student field to the current field
    def get_form_class(self):
        path = self.request.get_full_path() 
        std_list = path.split('/')
        std_pk = std_list[-1]
        modelform = super().get_form_class()
        modelform.base_fields['student'].limit_choices_to = {'pk': int(std_pk)}
        return modelform

class SubjectUpdate(UpdateView):
    model = Subject
    template_name = "subjectupdate.html"
    fields = ["name", "first_test", "second_test", "exam"]

class SubjectDelete(DeleteView):
    model = Subject
    template_name = "subjectdelete.html"


#-----------------------------------------------CLASSROOM VIEWS-------------------------------------------------
class ClassCreateView(CreateView):
    model = Classroom
    template_name = "classroomnew.html"
    fields = ["user","name", "form_teacher"]

    def get_form_class(self):
        modelform = super().get_form_class()
        modelform.base_fields['user'].limit_choices_to = {'username': self.request.user}
        return modelform
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

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('login')
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form':form})

def logout_view(request):
    logout(request)
    return redirect('index')


