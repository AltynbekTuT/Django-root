from django.contrib import admin
from django.contrib.admin import TabularInline, ModelAdmin  # Imports 1 & 2
from .models import Question, Choice, Submission, Lesson, Course  # Imports 3, 4, 5, 6, & 7

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['lesson', 'question_text']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date')
    search_fields = ['question_text']

class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course')
    search_fields = ['title']
    inlines = [QuestionInline]

admin.site.register(Course)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission)
