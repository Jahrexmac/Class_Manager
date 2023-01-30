from result.models import Classroom, Student, Subject

def subject_process (subjects):
        """
            this function adds the serial number, total and grade to the subject object
        """
        subject_obj= []
        serial_num = 0
        for subject in subjects:
            serial_num += 1
            total = subject.first_test + subject.second_test + subject.exam
            grade = grader(total)
            subject.total = total
            subject.grade = grade
            subject.serial_number = serial_num
            subject.remark = remark(grade)
            subject_obj.append(subject)
        return subject_obj

def subject_total(subjects):
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
def grader (total):
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

def result_display(students,subjects,student_pk, checker):

         #retrieve the class to get the pk so that the back key functionality would work for empty classes
    classroom = Classroom.objects.filter(name = students[0].student_class) 
    class_pk = classroom[0].pk
    all_students = Student.objects.filter(student_class = class_pk)
    all_students_totals = []
    all_processed_subjects = []

    for student in all_students:
        student_subjects = Subject.objects.filter(student = student.pk)
        student_subjects.position = '' # place holder for position
        processed_subject = subject_process(student_subjects)
        subject_totals = subject_total(processed_subject)
        all_processed_subjects.append(processed_subject)
        all_students_totals.append(subject_totals)
           

    sorted_totals = sort_score(all_students_totals) # for all student in the class
        
    results = student_grader(sorted_totals,all_students_totals) # returns all students result

    for result in results: # filter the result to only the student in focus
        std_name = students[0].first_name.title() + ' ' + students[0].last_name.title()
        pk = students[0].pk
        student_id = result['student_id']

        if checker: # if its a single student to build
            if student_id == student_pk:        
                subjects = subject_process(subjects)
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
    
def remark(grade):
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
        
def sort_score(all_students_totals):
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

def student_grader(sorted_totals,all_students_totals):
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
                    all_students_totals[j]['position'] = position(i+1) # Assign position of class
                    students_position.append(all_students_totals[j])

            j += 1
        i += 1
    return students_position

def position(num):
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