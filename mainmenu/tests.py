from django.test import TestCase, Client
from .models import Profile
from django.urls import reverse
from django.contrib.auth import get_user_model

from .views import borrowed_items, home_page_router


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

    def test_logged_in_borrowed_items(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('borrowed_items'))
        self.assertEqual(response.status_code, 200)

    def test_logged_in_profile(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)

    def test_logged_in_required_materials(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('required_materials'))
        self.assertEqual(response.status_code, 200)

    def test_not_logged_in(self):
        response = self.client.get(reverse('librarian_settings'))
        self.assertRedirects(response, '/accounts/login/?next=/librarian_settings/', status_code=302, target_status_code=200)

class PatronHomePageTests(TestCase):
    def setUp(self):
        self.client = Client()
        User = get_user_model()
        self.user, _ = User.objects.get_or_create(username='user4')
        self.user.set_password('pwd')
        self.user.save()
        self.profile, _ = Profile.objects.get_or_create(user=self.user, defaults={'userRole': 0})
        self.url = reverse('home_page')

    def test_logged_in_lent_items(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('lent_items'))
        self.assertEqual(response.status_code, 200)

    def test_logged_in_borrowed_items(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('borrowed_items'))
        self.assertEqual(response.status_code, 200)

    def test_logged_in_profile(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)

    def test_logged_in_required_materials(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('required_materials'))
        self.assertEqual(response.status_code, 200)

    def test_not_logged_in(self):
        response = self.client.get(reverse('lent_items'))
        self.assertRedirects(response, '/accounts/login/?next=/lent_items/', status_code=302, target_status_code=200)

class BorrowedItemsPageTestPatron(TestCase):
    def setUp(self):
        self.client = Client()
        User = get_user_model()
        self.user, _ = User.objects.get_or_create(username='user4')
        self.user.set_password('pwd')
        self.user.save()
        self.profile, _ = Profile.objects.get_or_create(user=self.user, defaults={'userRole': 0})
        self.owner = User.objects.get_or_create(username='user_alpha')
        self.borrower = User.objects.get_or_create(username='user_gamma')
        self.item = Item.objects.get_or_create(name='To be borrowed',status = Item.STATUS_AVAILABLE, location = 'Clark Hall', description = 'The item is for testing purposes only', owner = self.owner)
        self.base_url = reverse("home_page")
        self.client.force_login(self.user)
        self.gotten_into_url = reverse("borrowed_items")
        self.go_through = reverse("available_to_requested", args =[self.item.pk])
    def test_redirect_back_to_home_page(self):
        response = self.client.get(reverse("home_page"))
        self.assertEqual(response.status_code, 200)

    def test_form_if_request_is_sent(self):
        first_response = self.client.get(self.gotten_into_url)
        self.assertContains(first_response, "To be borrowed")
        borrowing = self.client.post(self.go_through)
        self.assertRedirects(borrowing,'/accounts/login/?next=/home_page/', status_code=302, target_status_code=200)
        self.item.refresh_from_db()
        self.assertEqual(self.item.status,Item.STATUS_REQUESTED)
        self.assertEqual(self.item.location, 'Clark Hall')
        self.assertEqual(self.item.borrower, self.borrower)
        aftermath = self.client.post(self.gotten_into_url)
        self.assertNotContains(aftermath, "To be borrowed")

class BorrowedItemsPageTestLibrarian(TestCase):
    def setUp(self):
        self.client = Client()
        User = get_user_model()
        self.user, _ = User.objects.get_or_create(username='user4')
        self.user.set_password('pwd')
        self.user.save()
        self.profile, _ = Profile.objects.get_or_create(user=self.user, defaults={'userRole': 1})
        self.owner = User.objects.get_or_create(username='user_theta')
        self.borrower = User.objects.get_or_create(username='user_chi')
        self.item = Item.objects.get_or_create(name='To be reviewed', status=Item.STATUS_REQUESTED,location='Clark Hall',description='The item is for testing purposes only',
                                                       owner=self.owner,
                                                    borrower=self.borrower)
        self.base_url = reverse("librarian_home_page")
        self.client.force_login(self.user)
        self.gotten_into_url = reverse("borrowed_items")
        self.go_through = reverse("requested_to_in_circulation", args=[self.item.pk])
        self.message = Message.objects.get_or_create(sender=self.borrower, recipient=self.owner)

    def test_redirect_back_to_home_page(self):
        response = self.client.get(reverse("librarian_home_page"))
        self.assertEqual(response.status_code, 200)

    def test_form_if_request_is_sent_yes(self):
        first_response = self.client.get(self.gotten_into_url)
        self.assertContains(first_response, "To be borrowed")
        due_date = timezone.localdate() + timezone.timedelta(days=7)
        response = self.client.post(self.url, {
            'item': self.item.pk,
            'yes': 'Confirm',
            'due_date': due_date
        })
        self.assertRedirects(borrowing,'/accounts/login/?next=/home_page/', status_code=302, target_status_code=200)
        self.item.refresh_from_db()
        self.assertEqual(self.item.status,Item.STATUS_IN_CIRCULATION)
        self.assertEqual(self.item.location, 'Clark Hall')
        self.assertEqual(self.item.borrower, self.borrower)
        self.assertEqual(self.item.due_date, due_date)
        aftermath = self.client.post(self.gotten_into_url)
        self.assertNotContains(aftermath, "To be borrowed")

        messages = Message.objects.filter(item=self.item, recipient=self.patron)
        self.assertTrue(messages.exists())
        self.assertRedirects(response, reverse('home_page_router'))

    def test_form_if_request_is_sent_no(self):
        first_response = self.client.get(self.gotten_into_url)
        self.assertContains(first_response, "To be borrowed")
        due_date = timezone.localdate() + timezone.timedelta(days=7)
        response = self.client.post(self.url, {
            'item': self.item.pk,
            'no': 'Deny',
        })
        self.assertRedirects(borrowing,'/accounts/login/?next=/home_page/', status_code=302, target_status_code=200)
        self.item.refresh_from_db()
        self.assertEqual(self.item.status,Item.STATUS_AVAILABLE)
        self.assertEqual(self.item.location, 'Clark Hall')
        self.assertIsNone(self.item.borrower)
        self.assertEqual(self.item.due_date, due_date)
        aftermath = self.client.post(self.gotten_into_url)
        self.assertNotContains(aftermath, "To be borrowed")

        messages = Message.objects.filter(item=self.item, recipient=self.patron)
        self.assertTrue(messages.exists())
        self.assertIn("denied", messages.last().content.lower())

        self.assertRedirects(response, reverse('home_page_router'))

class MarketPlaceTests(TestCase):
    def setUp(self):
        self.client = Client()
        User = get_user_model()
        self.user, _ = User.objects.get_or_create(username='user4')
        self.user.set_password('pwd')
        self.user.save()
        self.profile, _ = Profile.objects.get_or_create(user=self.user, defaults={'userRole': 1})
        self.owner = User.objects.get_or_create(username='user_theta')
        self.borrower = User.objects.get_or_create(username='user_chi')
        self.base_url = reverse("librarian_home_page")
        self.client.force_login(self.user)
        self.gotten_into_url = reverse("marketplace")
