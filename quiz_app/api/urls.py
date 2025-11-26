from django.urls import path, include
from .views import QuizCreateAPIView

urlpatterns = [
    path('create/', QuizCreateAPIView.as_view(), name='quiz-create'),
]