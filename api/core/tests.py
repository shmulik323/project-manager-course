# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase,Client,TransactionTestCase

from .models import UserProfileManager,UserProfile

class UserTestCase(TestCase):
    def setUp(self):
        user=UserProfileManager.objects.create_user("alexv@regular.com","alexvRegular","alex","vaitz")
        user.set_password("blayt1245")
        premium=UserProfileManager.objects.create_premium_user("alex@premium.com","alexvPremium","alex","vaitz","blyat12345","1234123412341234")
        premium.set_password("blyat12345")
        admin=UserProfileManager.objects.create_superuser("alex@admin.com","alexvAdmin","alex","vaitz","blayt12345")
        admin.set_password("blyat12345")
    
    def test_user_creation(self):
        user=UserProfileManager.objects.get(email="alexv@regular.com")
        self.assertTrue(isinstance(user))
        self.assertEqual(user.__unicode__(),user.email)

    def test_premium_creation(self):
        premium=UserProfileManager.objects.get(email="alex@premium.com")
        self.assertTrue(isinstance(premium))
        self.assertEqual(premium.__unicode__(),premium.email)

    def test_admin_creation(self):
        admin=UserProfileManager.objects.get(email="alex@admin.com")
        self.assertTrue(isinstance(admin))
        self.assertEqual(admin.__unicode__(),admin.email)

    def test_user_unique(self):
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
        
    def test_login(self):
        c=Client()
        login_success=c.login(email="alexv@regular.com", password="blayt1245")
        login_fail=c.login(email="bad_mail@regular.com", password="not12345")
        self.assertTrue(login_success)
        self.assertFalse(login_fail)
# Create your tests here.
