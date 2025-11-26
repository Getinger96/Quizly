from rest_framework import generics,viewsets,filters,status
from .serializers import QuizCreateSerializer
from ..models  import Quiz
import json
import yt_dlp
from rest_framework.response import Response
import whisper
from rest_framework.permissions import  AllowAny
from google import genai


def my_hook(d):
    if d['status'] == 'finished':
        return d

class QuizCreateAPIView(generics.CreateAPIView):
    serializer_class=QuizCreateSerializer
    queryset=Quiz.objects.all()
    permission_classes=[AllowAny]

    def post(self,request):
        URL=request.data.get('url')
        ydl_opts = { "format": "bestaudio/best",

    "outtmpl": 'media/audio.mp3',

    'verbose': True,

    "noplaylist": True,
    'progress_hooks': [my_hook],
    }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
          ydl.download(URL)

        model = whisper.load_model("tiny")
        result = model.transcribe("media/audio.mp3")
        transcript=result["text"]
        client = genai.Client()
        prompt=f"""Based on the following transcript, generate a quiz in valid JSON format.

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
           Transcript:
             {transcript}"""     
        response = client.models.generate_content(
           model="gemini-2.5-flash", contents=prompt)
        
        raw_output = response.candidates[0].content.parts[0].text
        raw_output = raw_output.strip().strip("```").replace("json", "")
        quiz_json = json.loads(raw_output)
        
        serializer=self.get_serializer(data=quiz_json)
        serializer.is_valid(raise_exception=True)
        serializer.save()


        return Response(serializer.data,status=status.HTTP_201_CREATED)

