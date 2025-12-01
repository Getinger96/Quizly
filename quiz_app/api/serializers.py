from rest_framework import serializers
from ..models import Quiz,Question
import json

class QuestionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Question
        fields=['id','question_title','question_options','answer','created_at','updated_at']

        def validate(self, data):
         options = data.get("question_options", [])
         answer = data.get("answer", "").strip()

         if answer not in options:
            raise serializers.ValidationError({
                "answer": f"Answer must be one of {options}"
            })

         return data


class QuizSerializer(serializers.ModelSerializer):
    URL=serializers.URLField(required=False,allow_null=True)
    class Meta:
        model=Quiz
        fields='__all__'

    

class QuizCreateSerializer(serializers.ModelSerializer):
    
    questions=QuestionSerializer(many=True,read_only=True)


    class Meta:
        model=Quiz
        fields=['title',
            'description',
            'created_at',
            'updated_at',
            'video_url',
            'questions']

    def create (self,validated_data):
        print(validated_data)
        questions_data= validated_data.pop('questions',[])
        print(validated_data)
        print(questions_data)
        quiz=Quiz.objects.create(**validated_data)
        for questions in questions_data:
            Question.objects.create(quiz=quiz,**questions)
            print(quiz)
        return quiz


        
            

