from rest_framework import serializers
from ..models import Quiz,Question
import json

class QuestionSerializer(serializers.ModelSerializer):
    """
    Serializer for individual quiz questions.
    Handles validation of the answer field to ensure it matches
    one of the provided question options.
    """

    class Meta:
        model=Question
        fields=['id','question_title','question_options','answer','created_at','updated_at']

        def validate(self, data):
         """
        Ensure that the provided answer exists within the question_options list.
        """
         options = data.get("question_options", [])
         answer = data.get("answer", "").strip()

         if answer not in options:
            raise serializers.ValidationError({
                "answer": f"Answer must be one of {options}"
            })

         return data


class QuizSerializer(serializers.ModelSerializer):
    """
    Read-only serializer used for retrieving quizzes.
    Includes nested questions.
    """
    questions=QuestionSerializer(many=True,read_only=True)
    class Meta:
        model=Quiz
        fields=['id','title','description','created_at','updated_at','video_url','questions']

class QuizCreateSerializer(serializers.ModelSerializer):
    """
    Serializer used for creating quizzes.
    Allows optional YouTube video URLs and converts youtu.be links
    into standard youtube.com/watch?v format.
    """
    video_url = serializers.URLField(
        required=False, allow_null=True, allow_blank=True
    )
    questions=QuestionSerializer(many=True,read_only=True)

    class Meta:
        model=Quiz
        fields=['title',
            'description',
            'created_at',
            'updated_at',
            'video_url',
            'questions']
        
    def validate_video_url(self, value):
        """
        Validates and normalizes YouTube URLs.

        Rules:
        - Empty or null URLs are allowed.
        - Standard YouTube URLs are left unchanged.
        - Short youtu.be links are transformed to youtube.com/watch?v format.
        - All other URLs are rejected.
        """
        if not value:
            return value  

        if "youtube.com/watch?v=" in value:
            return value

        if "youtu.be/" in value:
            
            video_id = value.split("/")[-1].split("?")[0]
            return f"https://www.youtube.com/watch?v={video_id}"

        raise serializers.ValidationError("Nur YouTube URLs erlaubt")

    def create (self,validated_data):
         """
        Creates a quiz instance. Question data is ignored here because
        questions are added later through a separate process.

        Returns:
            The created Quiz instance.
        """
         print(validated_data)
         questions_data= validated_data.pop('questions',[])
         print(validated_data)
         print(questions_data)
         if validated_data["video_url"]:"youtu.be"
         quiz=Quiz.objects.create(**validated_data)
         for questions in questions_data:
            Question.objects.create(quiz=quiz,**questions)
            print(quiz)
         return quiz


        
            

