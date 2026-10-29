
from django.contrib import admin

from .models import (
    Course,
    Lesson,
    Question,
    Choice,
    Submission,
    Enrollment,
    Instructor,
    Learner,
)


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ("question_text", "lesson", "grade")
    search_fields = ("question_text",)


class LessonAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ("title", "course")


admin.site.register(Course)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission)
admin.site.register(Enrollment)
admin.site.register(Instructor)
admin.site.register(Learner)
