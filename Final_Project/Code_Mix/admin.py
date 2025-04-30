from django.contrib import admin
from .models import Questions, Options, UserAnswer

# Register your models here.
@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):
    list_display = ['id', 'diff_level', 'question_category', 'title', 'question']
    search_fields = ('id', 'question_category', 'question')

@admin.register(Options)
class OptionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'option_1', 'option_2', 'option_3', 'option_4', 'answer')
    search_fields = ('id', 'answer', 'question__title')

@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'question', 'selected_option', 'is_correct', 'category', 'difficulty', 'created_at')
    list_filter = ('is_correct', 'category', 'difficulty', 'created_at')
    search_fields = ('user__username', 'question__title')
