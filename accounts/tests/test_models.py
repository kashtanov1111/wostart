from django.test import TestCase

from accounts.models import CustomUser, UserProfile

class CustomUserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        CustomUser.objects.create(
            email='test@mail.ru',
            username='test',
            first_name='Test',
            last_name='Testy',
            password='testpass123')
    
    def test_get_absolute_url(self):
        customuser = CustomUser.objects.get(id=1)
        self.assertEqual(customuser.get_absolute_url(), '/users/test/')

    def test_email_uniqueness(self):
        customuser = CustomUser.objects.get(id=1)
        unique = customuser._meta.get_field('email').unique
        self.assertEqual(unique, True)
