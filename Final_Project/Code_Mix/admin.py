from django.contrib import admin
from .models import Questions, Options, UserAnswer, QuizProgress, UserPerformance

@admin.register(Options)
class OptionsAdmin(admin.ModelAdmin):
    list_display = ('question_title','option_1', 'option_2', 'option_3', 'option_4', 'answer', 'explanation')
    list_filter = ('question__diff_level', 'question__question_category')

    def question_title(self, obj):
        return obj.question.title
    question_title.short_description = 'Question Title'


@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'diff_level', 'question_category', 'title')
    list_filter = ('diff_level', 'question_category')



@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    # Updated "catagory" -> "category"
    list_display = ('user', 'question', 'selected_option', 'is_correct', 'category', 'difficulty')
    list_filter = ('category', 'difficulty', 'is_correct')


@admin.register(QuizProgress)
class QuizProgressAdmin(admin.ModelAdmin):
    # Updated "catagory" -> "category" and removed "last_update"
    list_display = ('user_or_session', 'category', 'difficulty', 'current_question_id')
    # Add a property or update the queryset if you require "last_update"
    
    def user_or_session(self, obj):
        return obj.user or obj.session_key
    user_or_session.short_description = 'User/Session'


@admin.register(UserPerformance)
class UserPerformanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'current_category', 'current_difficulty', 'total_answered', 'total_correct', 'total_wrong')
    list_filter = ('current_category', 'current_difficulty')

