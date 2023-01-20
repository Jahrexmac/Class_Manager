
from django.shortcuts import render
from django.views.generic import ListView
from django.views import View
from .models import Classroom, Student, Subject
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormMixin
from django.urls import reverse_lazy, reverse
from django import forms
import io
from django.http import FileResponse
from utilities.result_generator import generate_result_pdf

# Create your views here.
class Home(View):
    def get(self, request):
        return render(request, 'index.html')

class ClassListView(ListView):
    model = Classroom
    template_name = "classroom.html"

class Results(View):
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

        class_result = StudentDetails.result_display(self,students,sub,student_pk,checker= False)
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

        class_result = StudentDetails.result_display(self,students,sub,student_pk,checker= False)
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
        return FileResponse(buffer, as_attachment=False,filename=f'{class_result[0]["student_class"]}_results.pdf')
#end pdf implement





class StudentListView(View):
    
    def get(self, request, pk):
        num_students = 0
        std = Student.objects.filter(student_class=pk)
        try:
            std_class = std[0].student_class
            num_students = len(std)
        except IndexError:
            std = Classroom.objects.filter(pk = pk)
            std_class = std[0].name
            class_pk = std[0].pk
            num_students = 0
            return render(request, 'students.html', {'class': std_class, 'class_pk': class_pk, 'num_students': num_students})
        else:
            return render(request, 'students.html', {'students': std, 'class': std_class, 'pk': pk, 'class_pk': pk, 'num_students': num_students})
    def post(self,request,pk):
        num_students = 0
        if 'save' in str(request.body):
            form = StudentNewForm(request.POST) #to save subject form
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
                return render(request, 'students.html', {'students': std, 'class': std_class, 'pk': pk, 'class_pk': class_pk, 'num_students': num_students})
      
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
      
class ClassCreateView(CreateView):
    model = Classroom
    template_name = "classroomnew.html"
    fields = ["name", "form_teacher"]

class StudentCreateView(CreateView):
    model = Student
    template_name = "studentnew.html"
    fields = ["student_class","first_name","last_name","middle_name","parent_name","parent_phone_number","house_address","religion"]

    def get_form_class(self):
        path = self.request.get_full_path() 
        class_pk = path[-2:]
        modelform = super().get_form_class()
        modelform.base_fields['student_class'].limit_choices_to = {'pk': int(class_pk)}
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

class StudentDetails(View):
    
    def get(self, request, pk):
        students = Student.objects.filter(pk = pk) # from data base
        subjects = Subject.objects.filter(student=pk) # from data base

        #subjects = self.subject_process(subjects) # refine the subjects list of subject object to include total, grade and serial number
        #return students, std_name, pk, class_pk, subjects and totals
        return render(request, 'studentdetails.html',self.result_display(students,subjects,pk, checker=True))
            
    def post(self,request,pk):
        if 'save' in str(request.body):
            form = SubjectNewForm(request.POST) #to save subject form
            if form.is_valid():
                form.save()
            
            subject = Subject.objects.last() # retrieve last object from the data base

            students = Student.objects.filter(pk= subject.student_id) # from data base
            subjects = Subject.objects.filter(student= subject.student_id) # from data base

            return render(request, 'studentdetails.html',self.result_display(students,subjects,subject.student_id, checker=True))
            
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

            return render(request, 'studentdetails.html',self.result_display(students,subjects, student_pk, checker=True))

        
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
            
            return render(request, 'studentdetails.html',self.result_display(students,subjects,pk, checker=True))
              
        if 'delete' in str(request.body):
            subject = Subject.objects.filter(pk = pk)
            
            student_pk = subject[0].student_id
            students = Student.objects.filter(pk = student_pk)
            subjects = Subject.objects.filter(student = student_pk) # from data base

            Subject.objects.filter(pk = pk ).delete() # deletes the student
            
            return render(request, 'studentdetails.html',self.result_display(students,subjects,student_pk, checker=True))

    def subject_process (self, subjects):
        """
            this function adds the serial number, total and grade to the subject object
        """
        subject_obj= []
        serial_num = 0
        for subject in subjects:
            serial_num += 1
            total = subject.first_test + subject.second_test + subject.exam
            grade = StudentDetails.grade(self, total)
            subject.total = total
            subject.grade = grade
            subject.serial_number = serial_num
            subject.remark = StudentDetails.remark(self,grade)
            subject_obj.append(subject)
        return subject_obj

    def subject_total(self, subjects):
        """
            Generate the grand total and average
        """
        try:
            if subjects[0].student_id:
                student_id = subjects[0].student_id
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
                return {'average': float(average), 'grand_total': grand_total, 'check': check, 'student_id': student_id, 'position': ''}
        except IndexError:
            return {'average': 0.00, 'grand_total': 0, 'check': False, 'student_id': 0, 'position': ''}
     

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

    def result_display(self,students,subjects,student_pk, checker):

         #retrieve the class to get the pk so that the back key functionality would work for empty classes
        classroom = Classroom.objects.filter(name = students[0].student_class) 
        class_pk = classroom[0].pk

#NEW CODE
        all_students = Student.objects.filter(student_class = class_pk)
        all_students_totals = []
        all_processed_subjects = []

        for student in all_students:
            student_subjects = Subject.objects.filter(student = student.pk)
            student_subjects.position = '' # place holder for position
            processed_subject = StudentDetails.subject_process(self, student_subjects)
            subject_totals = StudentDetails.subject_total(self, processed_subject)
            all_processed_subjects.append(processed_subject)
            all_students_totals.append(subject_totals)
           

        sorted_totals = StudentDetails.sort_score(self, all_students_totals) # for all student in the class
        
        results = StudentDetails.student_grader(self, sorted_totals,all_students_totals) # returns all students result

        for result in results: # filter the result to only the student in focus
            std_name = students[0].first_name.title() + ' ' + students[0].last_name.title()
            pk = students[0].pk
            student_id = result['student_id']

            if checker: # if its a single student to build
                if student_id == student_pk:        
#END OF NEW CODE
                    subjects = self.subject_process(subjects)
                    return {'students': students, 'name': std_name, 'pk': pk, 'class_pk': class_pk, 'subjects':subjects, 'result': result}
                if student_id == 0: #if no subject for student
                    return {'students': students, 'name': std_name, 'pk': pk, 'class_pk': class_pk, 'subjects':subjects, 'result': result}
            else: # builds class results
                class_result = []
                i = 0
                while i < len(all_processed_subjects):
                    j = 0
                    while j < len(all_processed_subjects):
                        if results[i]['student_id'] == all_students[j].pk and results[i]['student_id'] == all_processed_subjects[j][0].student_id:
                            results[i]['name'] = all_students[j]
                            results[i]['subject'] = all_processed_subjects[j]
                            results[i]['student_class'] = classroom[0].name
                            class_result.append(results[i]) # groups student to their result and subject
                        j +=1
                    i += 1
                return class_result
    
    def remark(self,grade):
        if grade == 'A':
            return 'Excellent'
        elif grade == 'B+':
            return 'Very Good'
        elif grade == 'B':
            return 'Good'
        elif grade == 'C':
            return 'Credit'
        elif grade == 'P':
            return 'Pass'
        else:
            return 'Fail'
        
    def sort_score(self, all_students_totals):
        """
        Returns the sorted score of all student
        from the largest to the smallest
        """
        i = 0
        score = []
        while i < len(all_students_totals):
            score.append(all_students_totals[i]['grand_total'])
            i += 1
        score = sorted(score, reverse=True)
        return score

    def student_grader(self,sorted_totals,all_students_totals):
        i = 0
        graded_student = []
        students_position = []
        while i < len(sorted_totals):
            j = 0
            while j < len(sorted_totals):
                if sorted_totals[i] == all_students_totals[j]["grand_total"]:  # check the current grand total against all student

                    if all_students_totals[j]['student_id'] in graded_student:  # check if student have been graded
                        break
                    else:
                        graded_student.append(all_students_totals[j]['student_id'])
                        all_students_totals[j]['position'] = StudentDetails.position(self, i+1) # Assign position of class
                        students_position.append(all_students_totals[j])

                j += 1
            i += 1
        return students_position

    def position(self,num):
        """
        Returns the position of each student
        """
        num = str(num)
        if num.endswith('1') and int(num) != 11:
            return (f"{num}st")
        elif num.endswith('2') and int(num) != 12:
            return (f"{num}nd")
        elif num.endswith('3') and int(num) != 13:
            return (f"{num}rd")
        else:
            return (f"{num}th")
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
    fields = ["first_name","last_name","middle_name","parent_name","parent_phone_number","house_address","religion"]
#"student_class",
class StudentRemove(DeleteView):
    model = Student
    template_name='removestudent.html'
    success_url = reverse_lazy('class')

class SubjectNew(CreateView):
    model = Subject
    template_name = "subjectnew.html"
    fields = ["student","name", "first_test", "second_test", "exam"]

#  To limit the student field to the current field
    def get_form_class(self):
        path = self.request.get_full_path() 
        std_pk = path[-2:]
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


# BACK FUNCTIONALITY FOR NEW STUDENT 