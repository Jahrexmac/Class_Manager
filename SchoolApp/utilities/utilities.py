from ..result import get_students

students = get_students()  # Retrieve the students information


def main():
    summary = [] # hold the result that can then be sorted for class positioning
    # create and fills subjects list based on subjects offered by the student
    i = 0
    while i < len(students):

        subjects = []
        for subject in students[i]["subjects"]:
            subjects.append(subject)

        # displays result of each student and return the result for class positioning
        summary.append(display_result(students[i], subjects))
        i += 1
    result_summary(summary)


# check subject grade
def grade(total):
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


# format the output of the individual test score so that it have a nice display
def score_length(score):
    """
    Returns the formated length of the score field
    during display to maintain a width of 2
    """
    if len(str(score)) == 1:
        return "0" + str(score)
    else:
        return score


# format the output of the total score so that it have a nice display
def total_score_length(total_score):
    """
    Returns the formated length of the total score field
    during display to maintain a width of 3
    """
    if len(str(total_score)) == 1:
        return "00" + str(total_score)
    elif len(str(total_score)) == 2:
        return "0" + str(total_score)
    else:
        return str(total_score)



# retrieve assessment details
def get_assessment(student, subjects, subjects_count):
    """
    Retrieve the accessment values from the
    student object and then return a calculated value for the accessment
    """
    # gets the first test, second test, exam and total of each subject
    first_test = (
        student["subjects"][subjects[subjects_count]]["first_test"]
        + student["subjects"][subjects[subjects_count]]["holiday_assignment"]
    )
    second_test = (
        student["subjects"][subjects[subjects_count]]["second_test"]
        + student["subjects"][subjects[subjects_count]]["project"]
    )
    exam = student["subjects"][subjects[subjects_count]]["exam"]
    total = first_test + second_test + exam

    return [
        score_length(first_test),
        score_length(second_test),
        score_length(exam),
        total_score_length(total),
        grade(total),
    ]


# format the length of the subject to maintain consistency in the display
def format_subject(subject):
    """
    Returns the formated length of the subject field
    during display to maintain a uniform width
    * the base value is used as the default width and can
    be modified to fit any desired width
    """
    base = 15
    if len(subject) < base:
        space = base - len(subject)
        return subject + (" " * space)
    else:
        return subject


# summary of result to display positions
def result_summary(summary):
    """
    Display the summary of all the student result
    indicating the names, grand total score,
    the average score and class position
    """
    sorted_score = sort_score(summary)
    student_grader(sorted_score, summary)


# store and sort the scores from biggest to smallest
def sort_score(result):
    """
    Returns the sorted score of all student
    from the largest to the smallest
    """
    i = 0
    score = []
    while i < len(result):
        score.append(result[i]["score"])
        i += 1
    score = sorted(score, reverse=True)
    return score


def summary_header():
    """
    Display the summary header
    """
    print(f"\n\n                                   RESULT SUMMARY           ")
    print(f"------------------------------------------------------------------------------------")
    print(f"                       Total   Average   Position\n")


def summary_base():
    """
    Display the result summary based
    """
    print(f"-------------------------------------------------------------------------------------")


# Assign Positions to student
def student_grader(score, result):
    """
    Assign class position to each student
    based on the sorted grand total score
    and display the position
    """
    summary_header()  # display the summary header
    i = 0
    graded_student = []
    while i < len(result):
        j = 0
        while j < len(result):
            if score[i] == result[j]["score"]:  # check the current grand total against all student

                if result[j]['name'] in graded_student:  # check if student have been graded
                    break
                else:
                    display_position(result, i, j)
                    graded_student.append(result[j]['name'])

            j += 1
        i += 1
    summary_base()  # display the summary base


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

# standardize student name length


def format_name(name):
    """
    Return a formated name field
    so that all names have equal field width
    """
    base = 20
    if len(name) < base:
        space = base - len(name)
        return name + (" " * space)
    else:
        return name


def format_ave(ave):
    """
    Format the average field width
    inorder to maintain 2 decimal place after the decimal point
    """
    if len(str(ave)) < 5:  # check for the width
        return str(ave) + '0'
    else:
        return ave

# display the position of student


def display_position(result, i, j):
    """
    Display the students names, grandtotal score,
    average and the class position
    """
    print(
        f"{format_name(result[j]['name'])}     {result[j]['score']}     {format_ave(result[j]['average'])}     {position(i+1)}")


def result_header(student):
    """
    Displays header of each student with their accessment categories
    """
    print(
        "======================================================================================================="
    )
    print(
        f"                                       {student['first_name']} {student['last_name']}"
    )
    print(
        "======================================================================================================="
    )
    print(
        f"                             1st Test    2nd Test    Exam    Total       Grade"
    )


def result_base(grand_total, average):
    """
    Display result base
    """
    print("")
    print(
        f"          Grade Total:{grand_total}          Average:{average}")
    print(
        "========================================================================================================"
    )


def display_result(student, subjects):
    """
    Display the result of each student
    """
    result_header(student)  # display result header
    grand_total = 0
    average = 0
    # loops through to get the assessment of each subjects and display it
    subjects_count = 0
    while subjects_count < len(subjects):
        first_test, second_test, exam, total, grade = get_assessment(
            student, subjects, subjects_count  # unpacking accessment value
        )
        print(
            f"{format_subject(subjects[subjects_count])}                 {first_test}          {second_test}        {exam}      {total}           {grade}"
        )
        # Accumulate the grand total from the total of each score
        grand_total = grand_total + int(total)
        subjects_count += 1

    average = grand_total / subjects_count
    average = f"{average:.2f}"

    # create a list of all student score
    result_total = {
        "name": f"{student['first_name']} {student['last_name']}",
        "score": grand_total,
        "average": float(average),
    }

    result_base(grand_total, average)  # display the base of the result

    return result_total


main()
