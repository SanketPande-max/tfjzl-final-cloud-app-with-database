
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Course, Lesson, Question, Choice, Submission, Enrollment


def course_details(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    return render(
        request,
        'course_details_bootstrap.html',
        {'course': course}
    )


@login_required
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    if request.method == 'POST':
        enrollment, created = Enrollment.objects.get_or_create(
            user=request.user,
            course=course
        )

        submission = Submission.objects.create(
            enrollment=enrollment
        )

        for key, value in request.POST.items():
            if key.startswith('question_'):
                selected_choice = get_object_or_404(
                    Choice,
                    pk=value
                )
                submission.choices.add(selected_choice)

        return redirect(
            'show_exam_result',
            course_id=course.id,
            submission_id=submission.id
        )

    return redirect('course_details', course_id=course.id)


@login_required
def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)

    submission = get_object_or_404(
        Submission,
        pk=submission_id,
        enrollment__course=course,
        enrollment__user=request.user
    )

    selected_ids = list(
        submission.choices.values_list('id', flat=True)
    )

    grade = 0
    possible = 0

    questions = Question.objects.filter(
        lesson__course=course
    )

    for question in questions:
        possible += question.grade

        if question.is_get_score(selected_ids):
            grade += question.grade

    passed = possible > 0 and (grade / possible) >= 0.8

    context = {
        'course': course,
        'submission': submission,
        'selected_ids': selected_ids,
        'grade': grade,
        'possible': possible,
        'passed': passed
    }

    return render(
        request,
        'exam_result_bootstrap.html',
        context
    )
