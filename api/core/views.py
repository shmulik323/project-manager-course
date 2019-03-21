# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from rest_framework import viewsets
from .serializers import UserSirializer
from .models import User
# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSirializer
    queryset = User
