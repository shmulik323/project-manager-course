# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from .models import UserProfileManager,UserProfile

# Create your tests here.

class UserTestCase(TestCase):
    def setUp(self):
        user=UserProfileManager.objects.create_user("alexv@regular.com","alexvRegular","alex","vaitz","blayt1245")
        premium=UserProfileManager.objects.create_premium_user("alex@premium.com","alexvPremium","alex","vaitz","blyat12345","1234123412341234")
        admin=UserProfileManager.objects.create_superuser("alex@admin.com","alexvAdmin","alex","vaitz","blayt1245")
    
    def test_user_creation(self):
        user=UserProfileManager.objects.get(email="alexv@regular.com")
        premium=UserProfileManager.objects.get(email="alex@premium.com")
        admin=UserProfileManager.objects.get(email="alex@admin.com")
        self.assertNotEqual(user,premium)
        self.assertNotEqual(user,admin)
        self.assertNotEqual(premium,admin)
    
    def test_premium(self):
        user=UserProfileManager.objects.get(email="alexv@regular.com")
        premium=UserProfileManager.objects.get(email="alex@premium.com")
        admin=UserProfileManager.objects.get(email="alex@admin.com")
        self.assertEqual(user.is_premium,False)
        self.assertEqual(premium.is_premium,True)
        self.assertEqual(admin.is_premium,False)
        

    