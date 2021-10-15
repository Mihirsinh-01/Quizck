from django.db import models

# Create your models here.

class Quiz(models.Model):
    hostname=models.CharField(max_length=15)
    quizId=models.CharField(max_length=100)
    questionNumber=models.IntegerField()
    question=models.CharField(max_length=500)
    option1=models.CharField(max_length=100)
    option2=models.CharField(max_length=100)
    option3=models.CharField(max_length=100)
    option4=models.CharField(max_length=100)
    answer=models.CharField(max_length=500)
    marks=models.IntegerField()
    timer=models.IntegerField()
    
    