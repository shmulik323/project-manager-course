from rest_framework import serializers

from .models import UserProfile,PremiumUserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    """A Serializer for our user profile object."""

    class Meta:
        model = UserProfile
        fields = ('id', 'user_name', 'email', 'first_name', 'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """Create and return a new user."""

        user = UserProfile(
        email = validated_data['email'],
        user_name = validated_data['user_name'],
        first_name = validated_data['first_name'],
        last_name = validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user

class PremiumUserProfileSerializer(serializers.ModelSerializer):
    """A Serializer for our user profile object."""

    class Meta:
        model = PremiumUserProfile
        fields = ('id','user_name', 'email', 'first_name', 'last_name', 'password', 'credit_card')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """Create and return a new premium user."""

        premium_user = PremiumUserProfile(
        email = validated_data['email'],
        user_name = validated_data['user_name'],
        first_name = validated_data['first_name'],
        last_name = validated_data['last_name'],
        credit_card = validated_data['credit_card']
        )

        premium_user.set_password(validated_data['password'])
        premium_user.save

        return premium_user