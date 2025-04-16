from django.db import models

# Create your models here.
Questions_rank = (
    (1, 'Bronze'),
    (2, 'Master'),
)
class Questions(models.Model):
    id = models.AutoField(primary_key=True)
    rank = models.IntegerField(choices=Questions_rank)
    title = models.CharField(max_length=100)
    question = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return f"{self.id} - {self.rank} - {self.title} - {self.question}"

class Options(models.Model):
    id = models.AutoField(primary_key=True)
    question_id = models.ForeignKey(Questions, on_delete=models.CASCADE)
    option_1 = models.CharField(max_length=100, null=True, blank=True)
    option_2 = models.CharField(max_length=100, null=True, blank=True)
    option_3 = models.CharField(max_length=100, null=True, blank=True)
    option_4 = models.CharField(max_length=100, null=True, blank=True)
    answer = models.CharField(max_length=100, null=True, blank=True)
    Questions = models.ForeignKey(Questions, on_delete=models.CASCADE, related_name='Options')

    def __str__(self):
        return f"{self.id} - {self.answer} {self.question_id} - {self.Questions}"
   
@property
def all_options(self):
    return [self.option_1, self.option_2, self.option_3, self.option_4]

