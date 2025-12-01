from django.db import models

# Create your models here.
class Quiz(models.Model):
  
  title=models.CharField(max_length=100)
  description=models.TextField()
  created_at=models.DateTimeField(auto_now_add=True)
  updated_at=models.DateTimeField(auto_now=True)
  video_url=models.URLField(blank=True,null=True)
  
  def __str__(self):
       return super().__str__() + self.title
 


class Question(models.Model):
    
 
    quiz=models.ForeignKey(Quiz,on_delete=models.CASCADE,related_name='questions')
    question_title=models.CharField(max_length=255)
    question_options=models.JSONField()
    answer=models.CharField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self):
       return super().__str__() + self.title
