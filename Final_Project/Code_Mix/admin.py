from django.contrib import admin
from .models import Questions, Options

# Register your models here.
@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):
    list_display = ['id', 'diff_level', 'question_category', 'title', 'question']
    search_fields = ('id', 'question_category', 'question')

@admin.register(Options)
class OptionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'question_id', 'option_1', 'option_2', 'option_3', 'option_4', 'answer')
    search_fields = ('id', 'answer','question')