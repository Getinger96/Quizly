from rest_framework import generics,viewsets,filters,status
from .serializers import QuizCreateSerializer,QuizSerializer
from ..models  import Quiz
import json
import yt_dlp
from rest_framework.response import Response
import whisper
from rest_framework.permissions import  AllowAny
from google import genai
import uuid
import os
from rest_framework.permissions import AllowAny, IsAuthenticated
from auth_app.api.permissions import IsCreator

def my_hook(d):
    if d['status'] == 'finished':
        return d

def video_donwload(self,request):
 URL=request.data.get('url')
 unique_id = uuid.uuid4().hex
 audio_path = f"media/audio_{unique_id}.mp3"
 ydl_opts = { "format": "bestaudio/best",

    "outtmpl": audio_path,

    'verbose': True,

    "noplaylist": True,
    'progress_hooks': [my_hook],
    }
 with yt_dlp.YoutubeDL(ydl_opts) as ydl:
          ydl.download(URL)
 return audio_path,URL

def transcript_video(self,audio_path):
 model = whisper.load_model("tiny")
 result = model.transcribe(audio_path)
 transcript=result["text"]
 return transcript

def build_prompt():
    return f"""Based on the following transcript, generate a quiz in valid JSON format.

The quiz must follow this exact structure:

{{

  "title": "Create a concise quiz title based on the topic of the transcript.",

  "description": "Summarize the transcript in no more than 150 characters. Do not include any quiz questions or answers.",

  "questions": [

    {{

      "question_title": "The question goes here.",

      "question_options": ["Option A", "Option B", "Option C", "Option D"],

      "answer": "The correct answer from the above question_options like Option A and no exact text"

    }},

    ...

    

  ]

}}

Requirements:
-(exactly 10 questions)

- Each question must have exactly 4 distinct answer options.

- Only one correct answer is allowed per question, and it must be present in 'question_options'.

- The output must be valid JSON and parsable as-is (e.g., using Python's json.loads).

- Do not include explanations, comments, or any text outside the JSON.
- DO NOT add code fences like ```json.
- DO NOT change the key names.
- DO NOT invent validation messages or reasoning. Only produce the JSON.
           """     


def generate_quiz(self,transcript):
   client = genai.Client()
   prompt_text = build_prompt()
   response = client.models.generate_content(
           model="gemini-2.5-flash", contents=prompt_text+transcript,
            
        )
        
   raw_output = response.text.strip()
   raw_output = (
   raw_output.replace("```json", "")
              .replace("```", "")
              .strip())
   quiz_json = json.loads(raw_output)
   return quiz_json
    

class QuizCreateAPIView(generics.CreateAPIView):
    serializer_class=QuizCreateSerializer
    queryset=Quiz.objects.all()
    permission_classes=[AllowAny]

    def post(self,request):
      
       video_donwload(self,request)
       audio_path,URL=video_donwload(self,request)
       transcript=transcript_video(self,audio_path)
       quiz_json=generate_quiz(self,transcript)

        
        
        
       quiz_json["video_url"] = URL  
       serializer=self.get_serializer(data=quiz_json)
       serializer.is_valid(raise_exception=True)
       serializer.save(questions=quiz_json["questions"],creator=self.request.user)
       return Response(serializer.data,status=status.HTTP_201_CREATED)


class QuizListView(generics.ListAPIView):
    
    serializer_class=QuizSerializer
    permission_classes=[IsAuthenticated,IsCreator]

    def get_queryset(self):
        return Quiz.objects.filter(creator=self.request.user)
    



class QuizDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class=QuizSerializer
    queryset=Quiz.objects.all()
    permission_classes=[IsAuthenticated,IsCreator]