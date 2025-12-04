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
    questions=QuestionSerializer(many=True,read_only=True)
    class Meta:
        model=Quiz
        fields=['id','title','description','created_at','updated_at','video_url','questions']

    

class QuizCreateSerializer(serializers.ModelSerializer):
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
        if not value:
            return value  # leer oder None ok

        # Wenn Link schon youtube.com ist → nichts ändern
        if "youtube.com/watch?v=" in value:
            return value

        # Wenn Link youtu.be ist → umwandeln
        if "youtu.be/" in value:
            # Video-ID extrahieren (alles nach youtu.be/)
            video_id = value.split("/")[-1].split("?")[0]
            return f"https://www.youtube.com/watch?v={video_id}"

        # alles andere ablehnen
        raise serializers.ValidationError("Nur YouTube URLs erlaubt")

    def create (self,validated_data):
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


        
            

