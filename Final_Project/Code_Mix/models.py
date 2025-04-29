from django.db import models
from django.contrib.auth.models import User
class Questions(models.Model):
    DIFFICULTY_LEVEL = (
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    )

    QUESTION_CATEGORY = (
        ('html', 'HTML'),
        ('python', 'Python'),
        ('django', 'Django'),
        ('isom', 'Isom'),
    )
    diff_level = models.CharField(max_length=10, choices=DIFFICULTY_LEVEL, null=True, blank=True)
    question_category = models.CharField(max_length=10, choices=QUESTION_CATEGORY, null=True, blank=True)
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    question = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return f"{self.id} - {self.diff_level} - {self.question_category} - {self.question} - {self.title}"

class Options(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE, related_name='options', null=True, blank=True)
    option_1 = models.CharField(max_length=100, null=True, blank=True)
    option_2 = models.CharField(max_length=100, null=True, blank=True)
    option_3 = models.CharField(max_length=100, null=True, blank=True)
    option_4 = models.CharField(max_length=100, null=True, blank=True)
    answer = models.CharField(max_length=100, null=True, blank=True)
    explanation = models.TextField(null=True, blank=True, help_text="Explanation for the correct answer")
    def __str__(self):
        return f"{self.id} - {self.answer} - {self.question}"

class UserAnswer(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_answers', null=True, blank=True)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE, related_name='user_answers')
    selected_option = models.CharField(max_length=100, null=True, blank=True)
    is_correct = models.BooleanField(default=False)
    category = models.CharField(max_length=10, choices=Questions.QUESTION_CATEGORY, null=True, blank=True)
    difficulty = models.CharField(max_length=10, choices=Questions.DIFFICULTY_LEVEL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} - {self.question} - {self.is_correct}"
    def save(self, *args, **kwargs):
        if self.question_id:
            question_obj = Questions.objects.get(id=self.question_id)
            self.category = question_obj.question_category
            self.difficulty = question_obj.diff_level

            option = Options.objects.get(question=self.question)
            self.is_correct = (self.selected_option == option.answer)
            super(UserAnswer, self).save(*args, **kwargs)
   
