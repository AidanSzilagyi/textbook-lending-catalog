from django.test import TestCase,Client
from .models import Profile
from django.urls import reverse
from django.contrib.auth import get_user_model

class LibProfileViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        User = get_user_model()
        self.user, _ = User.objects.get_or_create(username='user')
        self.user.set_password('passwerd')
        self.user.save()
        self.profile, _ = Profile.objects.get_or_create(user=self.user, defaults={'userRole': 1})
        self.url = reverse('librarian_home_page')

    def test_librarian_logged_in(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        # self.assertRedirects(response, '/librarian_home_page/', status_code=302, target_status_code=200)
        self.assertEqual(response.status_code, 200)

    def test_librarian_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, '/accounts/login/?next=/librarian_home_page/', status_code=302, target_status_code=200)

class PatronProfileViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        User = get_user_model()
        self.user, _ = User.objects.get_or_create(username='user2')
        self.user.set_password('passwd')
        self.user.save()
        self.profile, _ = Profile.objects.get_or_create(user=self.user, defaults={'userRole': 0})
        self.url = reverse('home_page')
    def test_logged_in(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    def test_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

class LibrarianHomePageTests(TestCase):
    def setUp(self):
        self.client = Client()
        User = get_user_model()
        self.user, _ = User.objects.get_or_create(username='user3')
        self.user.set_password('paswd')
        self.user.save()
        self.profile, _ = Profile.objects.get_or_create(user=self.user, defaults={'userRole': 1})
        self.url = reverse('librarian_home_page')
    def test_logged_in_librarian_settings(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('librarian_settings'))
        self.assertEqual(response.status_code, 200)
    def test_logged_in_lent_items(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('lent_items'))
        self.assertEqual(response.status_code, 200)
    def test_logged_in_marketplace(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('marketplace'))
        self.assertEqual(response.status_code, 200)
    def test_not_logged_in(self):
        response = self.client.get(reverse('librarian_settings'))
        self.assertRedirects(response, '/accounts/login/?next=/librarian_settings/', status_code=302, target_status_code=200)


