from django.db import models
from django.contrib.auth.models import User

class QuizCategory(models.Model):
    """
    Model representing a quiz category (HTML, Python, Django)
    """
    CATEGORY_CHOICES = (
        ('html', 'HTML'),
        ('python', 'Python'),
        ('django', 'Django'),
        ('isom', 'Isom'),
    )
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=10, choices=CATEGORY_CHOICES, unique=True)
    display_name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "Quiz Categories"
    
    def __str__(self):
        return self.display_name
        
class QuizDifficulty(models.Model):
    """
    Model representing a difficulty level (Easy, Medium, Hard)
    """
    DIFFICULTY_CHOICES = (
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    )
    
    id = models.AutoField(primary_key=True)
    level = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, unique=True)
    display_name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "Quiz Difficulty Levels"
    
    def __str__(self):
        return self.display_name

class Questions(models.Model):
    """
    Model representing quiz questions organized by category and difficulty level
    """
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
    
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    question = models.CharField(max_length=1000, null=True, blank=True)
    
    diff_level = models.CharField(max_length=10, choices=DIFFICULTY_LEVEL, null=True, blank=True)
    question_category = models.CharField(max_length=10, choices=QUESTION_CATEGORY, null=True, blank=True)
    
    quiz_category = models.ForeignKey(QuizCategory, on_delete=models.SET_NULL, related_name='questions', null=True, blank=True)
    quiz_difficulty = models.ForeignKey(QuizDifficulty, on_delete=models.SET_NULL, related_name='questions', null=True, blank=True)
    question_number = models.PositiveIntegerField(help_text="Question number within this category and difficulty (e.g., q1, q2, q3)", null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Questions"
        ordering = ['quiz_category', 'quiz_difficulty', 'question_number']
    
    def save(self, *args, **kwargs):
        if self.quiz_difficulty:
            self.diff_level = self.quiz_difficulty.level
        elif self.diff_level and not self.quiz_difficulty:
            difficulty, created = QuizDifficulty.objects.get_or_create(
                level=self.diff_level,
                defaults={'display_name': dict(self.DIFFICULTY_LEVEL).get(self.diff_level, '')}
            )
            self.quiz_difficulty = difficulty
            
        if self.quiz_category:
            self.question_category = self.quiz_category.name
        elif self.question_category and not self.quiz_category:
            category, created = QuizCategory.objects.get_or_create(
                name=self.question_category,
                defaults={'display_name': dict(self.QUESTION_CATEGORY).get(self.question_category, '')}
            )
            self.quiz_category = category
            
        super(Questions, self).save(*args, **kwargs)

    def __str__(self):
        category = self.quiz_category.display_name if self.quiz_category else self.question_category
        difficulty = self.quiz_difficulty.display_name if self.quiz_difficulty else self.diff_level
        return f"Q{self.question_number or self.id}: {category} - {difficulty} - {self.title}"

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
    
    quiz_category = models.ForeignKey(QuizCategory, on_delete=models.SET_NULL, related_name='user_answers', null=True, blank=True)
    quiz_difficulty = models.ForeignKey(QuizDifficulty, on_delete=models.SET_NULL, related_name='user_answers', null=True, blank=True)

    def __str__(self):
        return f"{self.id} - {self.question} - {self.is_correct}"
        
    def save(self, *args, **kwargs):
        if self.question:
            self.category = self.question.question_category
            self.difficulty = self.question.diff_level
            
            self.quiz_category = self.question.quiz_category
            self.quiz_difficulty = self.question.quiz_difficulty

            try:
                option = Options.objects.get(question=self.question)
                self.is_correct = (self.selected_option == option.answer)
            except Options.DoesNotExist:
                self.is_correct = False
                
        super(UserAnswer, self).save(*args, **kwargs)
        
class QuizProgress(models.Model):
    """
    Model tracking user progress in quizzes
    """
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_progress', null=True, blank=True)
    session_key = models.CharField(max_length=100, null=True, blank=True, help_text="For anonymous users")
    
    category = models.CharField(max_length=10, choices=Questions.QUESTION_CATEGORY, null=True, blank=True)
    difficulty = models.CharField(max_length=10, choices=Questions.DIFFICULTY_LEVEL, null=True, blank=True)
    
    quiz_category = models.ForeignKey(QuizCategory, on_delete=models.SET_NULL, related_name='quiz_progress', null=True, blank=True)
    quiz_difficulty = models.ForeignKey(QuizDifficulty, on_delete=models.SET_NULL, related_name='quiz_progress', null=True, blank=True)
    
    current_question_id = models.IntegerField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Quiz Progress"
        unique_together = [
            ['user', 'category', 'difficulty'], 
            ['session_key', 'category', 'difficulty'],
            ['user', 'quiz_category', 'quiz_difficulty'],
            ['session_key', 'quiz_category', 'quiz_difficulty']
        ]
        
    def save(self, *args, **kwargs):
        if self.quiz_category and not self.category:
            self.category = self.quiz_category.name
        elif self.category and not self.quiz_category:
            try:
                self.quiz_category = QuizCategory.objects.get(name=self.category)
            except QuizCategory.DoesNotExist:
                pass
                
        if self.quiz_difficulty and not self.difficulty:
            self.difficulty = self.quiz_difficulty.level
        elif self.difficulty and not self.quiz_difficulty:
            try:
                self.quiz_difficulty = QuizDifficulty.objects.get(level=self.difficulty)
            except QuizDifficulty.DoesNotExist:
                pass
                
        super(QuizProgress, self).save(*args, **kwargs)
        
    def __str__(self):
        user_identifier = self.user.username if self.user else f"Session: {self.session_key}"
        category = self.quiz_category.display_name if self.quiz_category else self.category
        difficulty = self.quiz_difficulty.display_name if self.quiz_difficulty else self.difficulty
        return f"{user_identifier} - {category} - {difficulty} - Question: {self.current_question_id}"
   
