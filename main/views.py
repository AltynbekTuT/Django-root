from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Lesson, Enrollment, Question, Choice, Submission


def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user = request.user
    enrollment = Enrollment.objects.get(user=user, course=course)

    if request.method == 'POST':
        submission = Submission.objects.create(enrollment=enrollment)
        for key, value in request.POST.items():
            if key.startswith('choice_'):
                choice_id = int(value)
                choice = get_object_or_404(Choice, pk=choice_id)
                submission.choices.add(choice)

        submission.save()
        return redirect('onlinecourse:show_exam_result', course_id=course.id, submission_id=submission.id)


def show_exam_result(request, course_id, submission_id):
    context = {}
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)

    selected_ids = [choice.id for choice in submission.choices.all()]

    total_score = 0
    possible_score = 0

    for question in course.question_set.all():
        possible_score += question.grade
        if question.is_get_score(selected_ids):
            total_score += question.grade

    grade = (total_score / possible_score) * 100 if possible_score > 0 else 0

    context['course'] = course
    context['submission'] = submission
    context['selected_ids'] = selected_ids
    context['grade'] = grade
    context['total_score'] = total_score
    context['possible_score'] = possible_score

    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)