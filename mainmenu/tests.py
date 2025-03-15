from django.test import TestCase, Client
from .models import Profile, create_user_profile
from django.urls import reverse
import requests
from django.contrib.auth.models import User




# Create your tests here.
class LibProfileViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.Profile = create_profile(user=create_user(username="user", password="passwerd"), userRole=1)
        self.url = reverse('librarian_homepage')

    def test_librarian_logged_in(self):
        self.client.login(username="user", password="passwerd")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_librarian_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)