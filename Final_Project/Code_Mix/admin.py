from django.contrib import admin
from .models import QuizCategory, QuizDifficulty, Questions, Options, UserAnswer, QuizProgress

# Register your models here.
@admin.register(QuizCategory)
class QuizCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'display_name']
    search_fields = ['name', 'display_name']
    
@admin.register(QuizDifficulty)
class QuizDifficultyAdmin(admin.ModelAdmin):
    list_display = ['id', 'level', 'display_name']
    search_fields = ['level', 'display_name']

@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):
    list_display = ['id', 'quiz_category', 'quiz_difficulty', 'question_number', 'title']
    list_filter = ['quiz_category', 'quiz_difficulty', 'question_category', 'diff_level']
    search_fields = ['title', 'question']
    
    readonly_fields = ['diff_level', 'question_category']

@admin.register(Options)
class OptionsAdmin(admin.ModelAdmin):
    list_display = ['id', 'question', 'option_1', 'option_2', 'option_3', 'option_4', 'answer']
    list_filter = ['question__quiz_category', 'question__quiz_difficulty', 'question__question_category', 'question__diff_level']
    search_fields = ['answer', 'question__title']

@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'question', 'selected_option', 'is_correct', 'created_at']
    list_filter = ['is_correct', 'quiz_category', 'quiz_difficulty', 'category', 'difficulty', 'created_at']
    search_fields = ['user__username', 'question__title']

@admin.register(QuizProgress)
class QuizProgressAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'quiz_category', 'quiz_difficulty', 'current_question_id', 'last_updated']
    list_filter = ['quiz_category', 'quiz_difficulty', 'category', 'difficulty', 'last_updated']
    search_fields = ['user__username']
