import unittest
from django.test import Client, TestCase
from django.contrib.auth.models import User
import string
import random
from django.test.utils import override_settings
from django.urls import reverse
from .models import Reviews, UserInformation, Request
from django.contrib.auth import get_user_model


class TestOAuth(TestCase):

    def test_create_new_user(self):
        num = 10
        # Randomly generating username
        username = ''.join(random.choices(string.ascii_uppercase + string.digits, k=num))
        # Receive key constraint if the same user is created with each test run
        # Randomly generate username to ensure repeatability
        user = User.objects.create(username=username)
        user.set_password('p@ssword')
        user.save()
        c = Client()
        logged_in = c.login(username=username, password='p@ssword')
        self.assertEqual(logged_in, True)

    def test_user_exists(self):
        c = Client()
        logged_in = c.login(username='testuser', password='123password123')
        self.assertEqual(logged_in, False)

    def test_login_fail(self):
        c = Client()
        logged_in = c.login(username='user-does-not-exist', password='no-password')
        self.assertEqual(logged_in, False)

    def test_admin_login(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username='admin',
            email='admin@gmail.com',
            password='1800xYz123P4B24'
        )
        self.client.force_login(self.admin_user)
        cookies = self.client.cookies
        self.assertTrue(cookies)


@override_settings(AUTHENTICATION_BACKENDS=
                   ('django.contrib.auth.backends.ModelBackend',))
class TestMapBox(TestCase):

    def test_load_page(self):
        num = 20
        # Randomly generating username
        username = ''.join(random.choices(string.ascii_uppercase + string.digits, k=num))
        # Receive key constraint if the same user is created with each test run
        # Randomly generate username to ensure repeatability
        user = User.objects.create(username=username)
        user.set_password('p@ssword')
        user.save()
        c = Client()
        logged_in = c.login(username=username, password='p@ssword')
        self.assertEqual(logged_in, True)
        response = c.get('/guide/map')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'UVA Guide')

    def test_load_map(self):
        num = 20
        # Randomly generating username
        username = ''.join(random.choices(string.ascii_uppercase + string.digits, k=num))
        # Receive key constraint if the same user is created with each test run
        # Randomly generate username to ensure repeatability
        user = User.objects.create(username=username)
        user.set_password('p@ssword')
        user.save()
        c = Client()
        logged_in = c.login(username=username, password='p@ssword')
        self.assertEqual(logged_in, True)
        response = c.get('/guide/map')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'guide-map')

    def test_load_geolocate(self):
        num = 20
        # Randomly generating username
        username = ''.join(random.choices(string.ascii_uppercase + string.digits, k=num))
        # Receive key constraint if the same user is created with each test run
        # Randomly generate username to ensure repeatability
        user = User.objects.create(username=username)
        user.set_password('p@ssword')
        user.save()
        c = Client()
        logged_in = c.login(username=username, password='p@ssword')
        self.assertEqual(logged_in, True)
        response = c.get('/guide/map')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'geo-button')

    def test_load_searchbar(self):
        num = 20
        # Randomly generating username
        username = ''.join(random.choices(string.ascii_uppercase + string.digits, k=num))
        # Receive key constraint if the same user is created with each test run
        # Randomly generate username to ensure repeatability
        user = User.objects.create(username=username)
        user.set_password('p@ssword')
        user.save()
        c = Client()
        logged_in = c.login(username=username, password='p@ssword')
        self.assertEqual(logged_in, True)
        response = c.get('/guide/map')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'search-bar')


class TestReviews(TestCase):

    def test_invalid_review(self):
        reviews = Reviews.objects.all()
        invalid = "Invalid Review"
        self.assertTrue(invalid not in reviews)

    def test_create_review(self):
        r = Reviews(location="Wilson Hall", review="My test review of Wilson Hall")
        r.save()
        r_location = r.location
        r_review = r.review
        self.assertTrue(r in Reviews.objects.all())
        self.assertTrue(r_location == "Wilson Hall")
        self.assertTrue(r_review == "My test review of Wilson Hall")

    def test_delete_review(self):
        r = Reviews(location="Ruffner Hall", review="My test review of Ruffner Hall")
        r.save()
        r_id = r.id
        r_location = r.location
        r_review = r.review
        self.assertTrue(r in Reviews.objects.all())
        self.assertTrue(r_location == "Ruffner Hall")
        self.assertTrue(r_review == "My test review of Ruffner Hall")
        Reviews.objects.filter(id=r_id).delete()
        reviews = Reviews.objects.all()
        self.assertTrue(r not in reviews)


def create_request(name, address):
    return Request.objects.create(name=name, address=address)


class TestRequest(TestCase):

    #source: https://stackoverflow.com/questions/60322847/how-to-test-admin-change-views
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username='testAdmin',
            email='admin@gmail.com',
            password='p@ssword'
        )
        self.client.force_login(self.admin_user)

    def test_valid_request_1(self):
        request = create_request("The Pav", "180 McCormick Rd Charlottesville, VA 22903")
        response = self.client.get(reverse("guide:csvView"))
        self.assertContains(response, "180 McCormick Rd Charlottesville, VA 22903")

    def test_valid_request_2(self):
        request = create_request("Rotunda", "1826 University Ave, Charlottesvile, VA 29904")
        response = self.client.get(reverse("guide:csvView"))
        self.assertContains(response, "1826 University Ave, Charlottesvile, VA 29904")

    def test_multiple_request(self):
        request = create_request("Rotunda", "1826 University Ave, Charlottesvile, VA 29904")
        response = self.client.get(reverse("guide:csvView"))
        self.assertContains(response, "1826 University Ave, Charlottesvile, VA 29904")
        request = create_request("The Pav", "180 McCormick Rd Charlottesville, VA 22903")
        response = self.client.get(reverse("guide:csvView"))
        self.assertContains(response, "180 McCormick Rd Charlottesville, VA 22903")


class TestUserInformation(TestCase):

    def test_enter_info(self):
        insert = UserInformation(address="Test", city="Test", state="TS", zipcode="11111", phone_number="3432342343")
        insert.save()
        obj = UserInformation.objects.get(address="Test")
        self.assertTrue(obj.address == "Test")

    def test_no_user(self):
        insert = UserInformation(address="Address", city="City", state="ST", zipcode="11111", phone_number="1234567890")
        insert.save()
        obj = UserInformation.objects.get(address="Address")
        self.assertTrue(obj.address == "Address")

    def test_valid_user(self):
        insert = UserInformation(address="853 West Main Street", city="Charlottesville", state="VA", zipcode="22903", phone_number="4349063068")
        insert.save()
        obj = UserInformation.objects.get(address="853 West Main Street")
        self.assertTrue(obj.address == "853 West Main Street")

    def test_invalid_user(self):
        insert = UserInformation(address="1400 Wertland Street", phone_number="9065551234")
        insert.save()
        obj = UserInformation.objects.get(address="1400 Wertland Street")
        self.assertEqual(obj.address == "1400 Wertland Street", True)


class TestAdminView(TestCase):

    def test_admin_access(self):
        admin_user = User.objects.create_superuser('admin', 'admin@gmail.com', 'p@assword123')
        c = Client()
        logged_in = c.login(username='admin', password='p@assword123')
        response = c.get('/request/download')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(logged_in, True)

    def test_non_admin_access(self):
        num = 10
        # Randomly generating username
        username = ''.join(random.choices(string.ascii_uppercase + string.digits, k=num))
        # Receive key constraint if the same user is created with each test run
        # Randomly generate username to ensure repeatability
        user = User.objects.create(username=username)
        user.set_password('p@ssword')
        user.save()
        c = Client()
        logged_in = c.login(username=username, password='p@ssword')
        self.assertEqual(logged_in, True)
        response = c.get('/request/download')
        # Status code should not be 200 (admin only access)
        self.assertNotEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
