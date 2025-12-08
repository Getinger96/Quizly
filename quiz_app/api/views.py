from rest_framework import generics,viewsets,filters,status
from .serializers import QuizCreateSerializer,QuizSerializer
from ..models  import Quiz
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from auth_app.api.permissions import IsCreator
from .helper import video_donwload,transcript_video,generate_quiz


    

class QuizCreateAPIView(generics.CreateAPIView):
    """
    API view to handle the creation of a Quiz.
    This view integrates video download, transcription, and
    AI-based quiz generation.
    """
    serializer_class=QuizCreateSerializer
    queryset=Quiz.objects.all()
    permission_classes=[IsAuthenticated]

    def post(self,request):
       """
        Handle POST request to create a quiz:
        1. Download audio from the provided YouTube URL.
        2. Transcribe the audio using Whisper.
        3. Generate quiz JSON using the transcript and AI model.
        4. Set the video_url in the generated quiz JSON.
        5. Serialize and save the quiz along with its questions.
        """
      
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
     """
    API view to list all quizzes created by the authenticated user.
    Applies custom permission to ensure that only the creator can access their quizzes.
    """
    
     serializer_class=QuizSerializer
     permission_classes=[IsAuthenticated,IsCreator]
    

     def get_queryset(self):
         """
        Return only quizzes created by the authenticated user.
        """
         return Quiz.objects.filter(creator=self.request.user)
    



class QuizDetailView(generics.RetrieveUpdateDestroyAPIView):
     """
    API view to retrieve, update, or delete a single quiz.
    Permissions ensure that only the quiz creator can perform these actions.
    """
     serializer_class=QuizSerializer
     queryset=Quiz.objects.all()
     permission_classes=[IsAuthenticated,IsCreator]