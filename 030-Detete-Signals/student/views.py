from django.shortcuts import render
from .models import Student, Teacher
from django.db import connection
from django.db.models import Q
from django.db.models import Q, Exists, OuterRef

# Part 2
#################################################################

def find_student_classroom(student: Student) -> str:
    qs = Student.objects.filter(
        ~Exists(
            # ... where the student's teacher
            # ... does not exist in the teacher model
            Teacher.objects.filter(
            firstname=OuterRef('teacher')
        )),
        # ... and the id is equal to the passed id
        id = student.id,
        # ... and the classroom is >= 5
        classroom__gte = 5,
        # ... and the classroom is < 8
        classroom__lt = 8
    ).first()

    if qs is None:
        # classrooms that ARE NOT in the range of 5 to 7,
        # are marked as Dirty
        return 'Dirty Classroom'
    else:
        # classrooms within the range of 5 to 7,
        # are marked as Clean
        return 'Clean Classroom'



def student_list_(request):

    posts = Student.objects.all()

    print(posts)
    print(posts.query)
    print(connection.queries)

    return render(request, 'output.html',{'posts':posts})

def student_list_(request):
    posts = Student.objects.filter(surname__startswith='austin') | Student.objects.filter(surname__startswith='baldwin')

    print(posts)
    print(connection.queries)

    return render(request, 'output.html',{'posts':posts})

def student_list(request):
    # posts = Student.objects.filter(
    #         Q(surname__startswith='austin') |
    #         ~Q (surname__startswith='baldwin') |
    #         Q (surname__startswith='avery-parker')
    #     )

    # posts = Student.objects.filter(
    #     # get all students where
    #     Exists(
    #         # ... where the student's teacher
    #         # ... is exists in the teacher model
    #         Teacher.objects.filter(
    #         firstname=OuterRef('teacher')
    #     ))
    # ).order_by('id')

    posts = Student.objects.filter(
        # get all students where
        ~Exists(
            # ... where the student's teacher
            # ... does not exist in the teacher model
            Teacher.objects.filter(
            firstname=OuterRef('teacher')
        )),
        # ... and where the age is greater than or equal to 18
        Q(age__gte = 18),
        # ... but less than 20
        Q(age__lt = 20)
    ).order_by('id')

    classroom_status = []
    for post in posts:
        status = find_student_classroom(post)
        classroom_status.append({
            'id':post.id,
            'firstname':post.firstname,
            'surname':post.surname,
            'age':post.age,
            'classroom':post.classroom,
            'classroom_state': status,
            'teacher':post.teacher
        })


    print(posts.query)

    """

    SELECT "student_student"."id", "student_student"."firstname",
    "student_student"."surname", "student_student"."age",
    "student_student"."classroom", "student_student"."teacher"

    FROM "student_student"
    WHERE EXISTS(
        SELECT (1) AS "a"
        FROM "student_teacher" U0
        WHERE U0."firstname" = ("student_student"."teacher")
        LIMIT 1
    ) ORDER BY "student_student"."id" ASC
    """

    res = {
        "data": classroom_status
    }

    # print(posts)
    # print(connection.queries)

    print(classroom_status)

    return render(request, 'output.html', res)