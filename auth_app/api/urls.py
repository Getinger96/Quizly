from django.urls import path, include
from .views import RegistrationView,CookieTokenObtainPairView,LogoutView,CookieRefreshView

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='registration'),
    path('login/', CookieTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', CookieRefreshView.as_view(), name='token_refresh'),
   
]