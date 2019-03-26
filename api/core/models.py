# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager

# Create your models here.

class UserProfileManager(BaseUserManager):
    """Helps Django work with our custom user model"""

    def create_user(self, email,user_name, first_name, last_name, password=None):
        """Creates a new user profile object."""

        if not email:
            raise ValueError("Users must have an email address.")

        email = self.normalize_email(email)
        user = self.model(email=email,user_name=user_name, first_name=first_name, last_name=last_name)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_premium_user(self, email,user_name, first_name, last_name, password, credit_card):
        """Creates a new premium user profile object."""

        if not email:
            raise ValueError("Users must have an email address.")

        email = self.normalize_email(email)
        premim_user = self.model(email=email,user_name=user_name, first_name=first_name, last_name=last_name, credit_card=credit_card)

        premim_user.set_password(password)
        premim_user.save(using=self._db)


        return premim_user

    def create_superuser(self, email,user_name, first_name, last_name, password):
        """Creates and savesa new superuser with given details."""

        user = self.create_user(email,user_name, first_name, last_name, password)

        user.is_superuser = True
        user.is_staff = True
        
        user.save(using=self._db)

        return user

class UserProfile(AbstractBaseUser,PermissionsMixin):
    """Reprsents a "user profile" inside our system"""
    
    email = models.EmailField(max_length=255, unique=True)
    user_name = models.CharField(unique=True,max_length=30)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name', 'first_name', 'last_name']

    def get_full_name(self):
        """Used to get a users full name."""

        return "{0} {1}".format(self.first_name,self.last_name)

    def get_short_name(self):
        """Used to get a users short name"""

        return self.first_name
    
    def change_is_premium(self):
        """Function to change to a premium user."""
        
        self.is_premium = True

    def __str__(self):
        """uses this when it needs to convert the object to a string."""

        return self.get_full_name()

class PremiumUserProfile(UserProfile):
    """Reprsents a "premium user profile" inside our system"""

    credit_card = models.CharField(max_length=16, unique=True)
    
    def change(self):
        self.change_is_premium()
    
    REQUIRED_FIELDS = ['credit_card']



# Create your models here.
