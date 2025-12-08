from rest_framework import generics,viewsets,filters,status
from .serializers import QuizCreateSerializer,QuizSerializer
from ..models  import Quiz
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from auth_app.api.permissions import IsCreator
from .helper import video_donwload,transcript_video,generate_quiz


    

class QuizCreateAPIView(generics.CreateAPIView):
    serializer_class=QuizCreateSerializer
    queryset=Quiz.objects.all()
    permission_classes=[IsAuthenticated]

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
    

    def get_permissions(self):
        if self.request.method == 'GET':
           
         print(bool(self.request.user and self.request.user.is_authenticated))
        return super().get_permissions()

    def get_queryset(self):
        return Quiz.objects.filter(creator=self.request.user)
    



class QuizDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class=QuizSerializer
    queryset=Quiz.objects.all()
    permission_classes=[IsAuthenticated,IsCreator]