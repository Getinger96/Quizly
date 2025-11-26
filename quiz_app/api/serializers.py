from rest_framework import serializers
from ..models import Quiz,Question
import json
import yt_dlp
import whisper


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Question
        fields=['id','question_title','question_options','answer','created_at','updated_at']


class QuizSerializer(serializers.ModelSerializer):
    URL=serializers.URLField(required=False,allow_null=True)
    class Meta:
        model=Quiz
        fields='__all__'

    

class QuizCreateSerializer(serializers.ModelSerializer):
    url=serializers.URLField(required=False,allow_null=True)
    questions=QuestionSerializer(many=True,required=False)


    class Meta:
        model=Quiz
        fields=['url','questions']

    def create (self,validated_data):
        questions_data= validated_data.pop('questions',[])
        quiz=Quiz.objects.create(**validated_data)
        for questions_data in questions_data:
            Question.objects.create(quiz=quiz,**questions_data)
        return quiz


        
            

