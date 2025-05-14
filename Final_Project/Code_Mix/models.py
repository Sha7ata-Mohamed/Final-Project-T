from django.db import models 
from django.views.generic import TemplateView
from django.contrib.auth.models import User 

DIFFICULTY_LEVEL = [
    ('easy', 'Easy'),
    ('medium', 'Medium'),
    ('hard', 'Hard'),
]

QUESTION_CATEGORY = [
    ('html', 'HTML'),
    ('python', 'Python'),
    ('django', 'Django'),
]

class Questions(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    question = models.CharField(max_length=1000, null=True, blank=True)
    diff_level = models.CharField(max_length=10, choices=DIFFICULTY_LEVEL, null=True, blank=True)
    question_category = models.CharField(max_length=10, choices=QUESTION_CATEGORY, null=True, blank=True)
    answered_by = models.ManyToManyField(User, through='UserAnswer', related_name='answered_questions', blank=True)

    def __str__(self):
        return f"{self.id}: {self.diff_level} - {self.question_category} ({self.question})"

class Options(models.Model):
    question = models.OneToOneField(Questions, on_delete=models.CASCADE, null=True, blank=True, help_text="Question for which this option is valid")
    option_1 = models.CharField(max_length=255, default='')
    option_2 = models.CharField(max_length=255, default='')
    option_3 = models.CharField(max_length=255, default='')
    option_4 = models.CharField(max_length=255, default='')
    answer = models.CharField(max_length=255, default='')
    explanation = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Options for question {self.question.id if self.question else 'N/A'}"

class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=255, null=True, blank=True)
    is_correct = models.BooleanField()
    category = models.CharField(max_length=10, null=True, blank=True)
    difficulty = models.CharField(max_length=10, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answer by {self.user} for question {self.question.id} at time {self.timestamp}"

class QuizProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    category = models.CharField(max_length=10, null=True, blank=True)
    difficulty = models.CharField(max_length=10, null=True, blank=True)
    current_question_id = models.IntegerField(default=1)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Progress of {self.user or self.session_key} - {self.category} {self.difficulty}"

class UserPerformance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_category = models.CharField(max_length=10, choices=QUESTION_CATEGORY, null=True, blank=True, help_text="Category the user is currently working on")
    current_difficulty = models.CharField(max_length=10, choices=DIFFICULTY_LEVEL, null=True, blank=True, help_text="Difficulty level the user is currently working on")
    categories_started = models.JSONField(default=list, blank=True, help_text="List of categories the user has started")
    categories_finished = models.JSONField(default=list, blank=True, help_text="List of categories the user has completed")
    total_answered = models.IntegerField(default=0)
    total_correct = models.IntegerField(default=0)
    total_wrong = models.IntegerField(default=0)

    def __str__(self):
        return (
            f"Performance of {self.user.username}: "
            f"Category={self.current_category or 'N/A'}, "
            f"Difficulty={self.current_difficulty or 'N/A'}, "
            f"Answered={self.total_answered}, "
            f"Correct={self.total_correct}, Wrong={self.total_wrong}"
        )
    