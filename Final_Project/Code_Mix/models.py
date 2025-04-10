from django.db import models

# Create your models here.
def questions(request):
    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    question = models.CharField(max_length=1000)

def options(request):
    id = models.AutoField(primary_key=True)
    question_id = models.ForeignKey(questions, on_delete=models.CASCADE)
    option = models.CharField(max_length=1000)