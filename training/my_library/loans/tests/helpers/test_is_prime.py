from django.test import TestCase

# Create your tests here.

from loans.templates.helpers import is_prime

class IsPrimeTests(TestCase):
    def test_3_is_prime(self):
        self.assertTrue(is_prime(3))
    def test_4_is_not_prime(self):
        self.assertFalse(is_prime(4))