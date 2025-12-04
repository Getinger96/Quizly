from django.urls import path, include
from .views import QuizCreateAPIView, QuizListView,QuizDetailView

urlpatterns = [
    path('create/', QuizCreateAPIView.as_view(), name='quiz-create'),
    path('quizzes/',QuizListView.as_view(),name='quiz-list'),
    path('quizzes/<int:pk>/',QuizDetailView.as_view(),name='quiz-detail'),
]