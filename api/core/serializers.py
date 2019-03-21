
from rest_framework import serializers

from .models import  User

class UserSirializer(serializers.ModelSerializer):
    

    class Meta:
        model=User
        fields=("id","First_name","Last_name","Email","Password ")  