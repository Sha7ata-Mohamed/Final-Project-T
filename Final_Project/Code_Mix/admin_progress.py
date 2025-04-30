from django.contrib import admin
from .models_progress import UserProgress

class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'difficulty', 'current_question', 'updated_at')
    list_filter = ('category', 'difficulty', 'updated_at')
    search_fields = ('user__username', 'category', 'difficulty')
    date_hierarchy = 'updated_at'

admin.site.register(UserProgress, UserProgressAdmin)
