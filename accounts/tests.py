from django.test import TestCase
from django.contrib.auth import get_user_model


class UserManagersTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(username="justauser", email="just@user.com", password="qwe123QWE!@#")
        self.assertEqual(user.username, "justauser")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            self.assertFalse(user.last_name)
        except AttributeError:
            ...
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email="")
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", username="", password="qwe123QWE!@#")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(username="gigauser", email="giga@user.com", password="qwe123QWE!@#")
        self.assertEqual(admin_user.email, "giga@user.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            self.assertFalse(admin_user.first_name)
        except AttributeError:
            ...
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                username="gigauserr", email="giga@user.com", password="qwe123QWE!@#", is_superuser=False
            )
