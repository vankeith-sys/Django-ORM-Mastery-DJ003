from django.shortcuts import render
from .models import Student, Teacher
from django.db import connection
from django.db.models import Q
from django.db.models import Q, Exists, OuterRef

# Part 2
#################################################################
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

    posts = Student.objects.filter(
        Exists(Teacher.objects.filter(
            firstname=OuterRef('teacher')
        ))
    ).order_by('id')

    print(posts.query)

    """
    SELECT "student_student"."id", "student_student"."firstname",
    "student_student"."surname", "student_student"."age",
    "student_student"."classroom", "student_student"."teacher"

    FROM "student_student"
    WHERE EXISTS(
        SELECT (1) AS "a"
        FROM "student_student" U0
        WHERE U0."teacher" = ("student_student"."teacher")
        LIMIT 1
    ) ORDER BY "student_student"."id" ASC
    ____________________________

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


    data = []
    for post in posts:
        data.append({
            'id':post.id,
            'firstname':post.firstname,
            'surname':post.surname,
            'age':post.age,
            'classroom':post.classroom,
            'teacher':post.teacher
        })
    res = {
        "data": data
    }

    # print(posts)
    # print(connection.queries)

    print(data)

    return render(request, 'output.html', res)