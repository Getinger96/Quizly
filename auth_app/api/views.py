from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .serializers import RegistrationSerializer,CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from rest_framework_simplejwt.tokens import RefreshToken , AccessToken

class RegistrationView(APIView):
    """
    API view responsible for handling user registration.
    Accepts username, email, password, and confirmed_password.
    Returns 201 if the user is successfully created.
    """
    permission_classes = [AllowAny]

    def post(self, request):
         """
        Handle POST request for creating a new user.
        Validates the serializer and returns an appropriate response.
        """
         serializer = RegistrationSerializer(data=request.data)

         data = {}
         if serializer.is_valid():
            saved_account = serializer.save()
            data = {
                'username': saved_account.username,
                'email': saved_account.email,
                'user_id': saved_account.pk
            }
            return Response({"detail":'User created successfully!'},status=status.HTTP_201_CREATED)
         else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


class CookieTokenObtainPairView(TokenObtainPairView):
    """
    Custom login view that issues JWT tokens and stores
    both access and refresh tokens inside HTTP-only cookies.
    """
    serializer_class=CustomTokenObtainPairSerializer
    def post(self, request, *args, **kwargs):
         """
        Validate login credentials using the serializer.
        If valid, return user info and set JWT tokens as cookies.
        """
         serializer=self.get_serializer(data=request.data)
         if serializer.is_valid(raise_exception=True):
            data={
                'id':serializer.user.id,
                'username':serializer.user.username,
                'email':serializer.user.email
            } 
         refresh = serializer.validated_data["refresh"]
         access= serializer.validated_data["access"]
        
         response =Response({"detail":"Login succesfully!","user":data},status=status.HTTP_200_OK)

         """
        Set secure HttpOnly cookies containing JWT tokens.
        These cookies cannot be accessed via JavaScript and 
        are only sent automatically with requests.
        """

         response.set_cookie(
            key= "access_token",
            value= access,
            httponly=True,
            secure=True,
            samesite="Lax"
        )

         response.set_cookie(
            key= "refresh_token",
            value= refresh,
            httponly=True,
            secure=True,
            samesite="Lax"

        )
        
         return response 
    

class LogoutView(APIView):
     """
    API view for logging out a user.
    Deletes the refresh token by blacklisting it and
    removes the cookie from the client.
    """
     permission_classes=[IsAuthenticated]
     def post(self,request):
        refresh_token=request.COOKIES.get("refresh_token")
        refresh_token=RefreshToken(refresh_token)
        refresh_token.blacklist()
        response=Response()
        response.delete_cookie("refresh_token")
        response.data={"detail":"Logout successfully! All Tokens will be deleted. Refresh token is now invalid"}
        return response
    


class CookieRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
         """
        Handle POST request to invalidate the refresh token.
        Removes refresh_token cookie and blacklists the token.
        """
         refresh_token=request.COOKIES.get("refresh_token")
         """
        Convert the token into a RefreshToken object.
        This allows the token to be blacklisted.
        """
         if refresh_token is None:
            return Response({"detail":"Refresh token not found!"},
                            status=status.HTTP_400_BAD_REQUEST)
         serializer=self.get_serializer(data={"refresh":refresh_token})
         try:
            serializer.is_valid(raise_exception=True)
         except:
             return Response({"detail":"Refresh token invalid!"},
                            status=status.HTTP_401_UNAUTHORIZED)
         access_token=serializer.validated_data.get("access")
         response=Response({"detail":" Token refreshed",'access':access_token})
         """
        Save the new access token as an HttpOnly cookie.
        This cookie replaces the old access token.
        """
         response.set_cookie(
            key= "access_token",
            value= access_token,
            httponly=True,
            secure=True,
            samesite="Lax"
        )
         return response