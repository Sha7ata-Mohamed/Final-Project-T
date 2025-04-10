from django.contrib import admin
from .models import Questions, Options
# Register your models here.
@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'rank', 'title', 'question')
    search_fields = ('id','rank', 'title')

@admin.register(Options)
class OptionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'question_id', 'option_1', 'option_2', 'option_3', 'option_4', 'answer')
    search_fields = ('id','question_id')