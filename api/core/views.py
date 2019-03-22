# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets

from .serializers import UserProfileSerializer, PremiumUserProfileSerializer
from .models import UserProfile,PremiumUserProfile

# Create your views here.

class HelloApiView(APIView):
    """Test API View"""

    serializer_class = UserProfileSerializer

    def get(self, request, format=None):
        """Returns a list of APIView features"""

        an_apiview = [
        'Uses HTTP methods as function (get, post, patch, put, delete)',
        'It is similar to a tradirional Django view',
        'Gives you the most control over your logic',
        'Is mapped manually to URLs'
        ]

        return Response({'massage':'Hello','an_apiview':an_apiview})

    def post(self,request):
        """Create a hello message with our name."""

        serializer = UserProfileSerializer(data=request.data)

        if serializer.is_valid():
            name = serializer.data.get('name')
            message = 'Hello {0}'.format(name)
            return Response({'message':message})
        else:
            return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        """Handles updating an objact."""

        return Response({'method':"put"})

    def patch(self, request, pk=None):
        """Patch request, only updates fields provided in the request."""

        return Response({'method':'patch'})

    def delete(self, request, pk=None):
        """Deletes an object."""

        return Response({'method':'delete'})

class UserProfileViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating profiles."""

    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()

class PremiumUserProfileViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating profiles."""

    serializer_class = PremiumUserProfileSerializer
    queryset = PremiumUserProfile.objects.all()
# Create your views here.
