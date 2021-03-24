from django.contrib import admin
from quiz.base.models import Question
# Register your models here.

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'statement', 'available')
