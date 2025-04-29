from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

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
    def __str__(self):
        return f"{self.id} - {self.answer} - {self.question}"
   
class UserAnswer(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers', null=True, blank=True)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE, related_name='user_answers')
    selected_option = models.CharField(max_length=100, null=True, blank=True)
    is_correct = models.BooleanField(default=False)
    category = models.CharField(max_length=10, choices=Questions.QUESTION_CATEGORY, null=True, blank=True)
    difficulty = models.CharField(max_length=10, choices=Questions.DIFFICULTY_LEVEL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.id} - {self.question} - {self.is_correct}"
    def save(self, *args, **kwargs):
        # Make sure the question is saved before accessing its attributes
        if self.question_id:
            question_obj = Questions.objects.get(id=self.question_id)
            self.category = question_obj.question_category
            self.difficulty = question_obj.diff_level
            
            option = Options.objects.get(question=self.question)
            self.is_correct = (self.selected_option == option.answer)
            super(UserAnswer, self).save(*args, **kwargs)

class QuizSession(models.Model):
    """
    Model to track complete quiz attempts by users.
    This allows for better analytics and user history tracking.
    Also supports saving progress so users can resume from where they left off.
    """
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_sessions')
    category = models.CharField(max_length=10, choices=Questions.QUESTION_CATEGORY)
    difficulty = models.CharField(max_length=10, choices=Questions.DIFFICULTY_LEVEL)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    total_questions = models.PositiveIntegerField(default=0)
    correct_answers = models.PositiveIntegerField(default=0)
    score_percentage = models.FloatField(default=0.0)
    current_question = models.ForeignKey(Questions, on_delete=models.SET_NULL, null=True, blank=True, related_name='current_sessions')
    last_activity = models.DateTimeField(auto_now=True)
    is_paused = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username} - {self.category} - {self.difficulty} - {self.score_percentage}%"
    
    def calculate_score(self):
        """Calculate the score based on user answers in this session."""
        user_answers = UserAnswer.objects.filter(
            user=self.user,
            category=self.category,
            difficulty=self.difficulty,
            created_at__gte=self.start_time,
            created_at__lte=self.end_time or timezone.now()
        )
        
        self.total_questions = user_answers.count()
        self.correct_answers = user_answers.filter(is_correct=True).count()
        
        if self.total_questions > 0:
            self.score_percentage = (self.correct_answers / self.total_questions) * 100
        else:
            self.score_percentage = 0
        
        return self.score_percentage
    
    def complete_session(self):
        """Mark the session as completed and calculate final score."""
        self.end_time = timezone.now()
        self.is_completed = True
        self.is_paused = False
        self.current_question = None
        self.calculate_score()
        self.save()
    
    def pause_session(self, current_question):
        """Save the user's progress to resume later."""
        self.current_question = current_question
        self.is_paused = True
        self.save()
    
    def resume_session(self):
        """Resume a paused quiz session."""
        self.is_paused = False
        self.save()
        return self.current_question
    
    def update_progress(self, current_question):
        """Update the current question without pausing."""
        self.current_question = current_question
        self.save()
        
    def get_duration(self):
        """Get the duration of the quiz session in minutes."""
        end = self.end_time or timezone.now()
        duration = end - self.start_time
        return round(duration.total_seconds() / 60, 2)  # Return minutes
    
    @classmethod
    def get_active_session(cls, user, category, difficulty):
        """Get the user's active (incomplete and not paused) session for this category/difficulty."""
        return cls.objects.filter(
            user=user,
            category=category,
            difficulty=difficulty,
            is_completed=False,
            is_paused=False
        ).order_by('-start_time').first()
    
    @classmethod
    def get_paused_session(cls, user, category, difficulty):
        """Get the user's paused session for this category/difficulty."""
        return cls.objects.filter(
            user=user,
            category=category,
            difficulty=difficulty,
            is_completed=False,
            is_paused=True
        ).order_by('-last_activity').first()
   
