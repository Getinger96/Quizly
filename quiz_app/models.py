from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Quiz(models.Model):
  """
    Model representing a Quiz entity.

    Fields:
        title (CharField): The title of the quiz, max length 100.
        description (TextField): Detailed description of the quiz.
        created_at (DateTimeField): Timestamp when the quiz was created.
        updated_at (DateTimeField): Timestamp when the quiz was last updated.
        video_url (URLField): Optional URL to a related YouTube video.
        creator (ForeignKey): The user who created the quiz.
    """
  
  title=models.CharField(max_length=100)
  description=models.TextField()
  created_at=models.DateTimeField(auto_now_add=True)
  updated_at=models.DateTimeField(auto_now=True)
  video_url=models.URLField(blank=True,null=True)
  creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quizzes')
  
  def __str__(self):
       """
        Return a string representation of the Quiz.
        Currently appends the title to the default string.
        """
       return super().__str__() + self.title
 


class Question(models.Model):
    """
    Model representing a single question within a quiz.

    Fields:
        quiz (ForeignKey): The parent Quiz this question belongs to.
        question_title (CharField): The question text.
        question_options (JSONField): A list of possible answers.
        answer (CharField): The correct answer, must be one of question_options.
        created_at (DateTimeField): Timestamp when the question was created.
        updated_at (DateTimeField): Timestamp when the question was last updated.
    """
    
    quiz=models.ForeignKey(Quiz,on_delete=models.CASCADE,related_name='questions')
    question_title=models.CharField(max_length=255)
    question_options=models.JSONField()
    answer=models.CharField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
       """
        Return a string representation of the Question.
        Appends the question title to the default string.
        """
       return super().__str__() + self.title
