from django.db import models
from django.contrib.auth.models import User
from .models import Questions

class UserProgress(models.Model):
    """
    Model to store user progress in quizzes so they can resume later.
    This is kept separate from the main models.py to avoid modifying existing code.
    """
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress')
    current_question = models.ForeignKey(Questions, on_delete=models.CASCADE, related_name='user_progress')
    difficulty = models.CharField(max_length=10, choices=Questions.DIFFICULTY_LEVEL)
    category = models.CharField(max_length=10, choices=Questions.QUESTION_CATEGORY)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.category} - {self.difficulty} - Question {self.current_question.id}"
