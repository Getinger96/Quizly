from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView






class IsCreator(BasePermission):
    """
    Custom permission ensuring that only the creator of an object
    is allowed to access or modify it.
    """
    def has_object_permission(self, request, view, obj):
        """
        Check whether the requesting user is the creator of the object.
        Returns True only if the object's creator matches the current user.
        """
        
        return obj.creator == request.user
    


