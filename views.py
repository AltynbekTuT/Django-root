from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Course, Question, Choice, Submission

@login_required
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        Submission.objects.filter(user=request.user, question__lesson__course=course).delete()
        questions = Question.objects.filter(lesson__course=course)
        for question in questions:
            choice_id = request.POST.get(f"question_{question.id}")
            if choice_id:
                selected_choice = get_object_or_404(Choice, pk=choice_id)
                Submission.objects.create(
                    user=request.user,
                    question=question,
                    selected_choice=selected_choice
                )
        return redirect('onlinecourse:show_exam_result', course_id=course.id)
    return redirect('onlinecourse:course_details', course_id=course.id)

@login_required
def show_exam_result(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    submissions = Submission.objects.filter(user=request.user, question__lesson__course=course)
    total_questions = Question.objects.filter(lesson__course=course).count()
    correct_answers = sum(1 for sub in submissions if sub.selected_choice.is_correct)
    
    score = (correct_answers / total_questions * 100) if total_questions > 0 else 0
    passed = score >= 70
    
    context = {
        'course': course,
        'score': round(score, 1),
        'correct_answers': correct_answers,
        'total_questions': total_questions,
        'passed': passed,
        'submissions': submissions
    }
    return render(request, 'onlinecourse/exam_result.html', context)
