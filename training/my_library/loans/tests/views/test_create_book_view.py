from django.test import TestCase
from django.urls import reverse
from loans.forms import BookForm
from loans.models import Book

class CreateBookTestCase(TestCase):
    def setUp(self):
        self.url = reverse('create_book')
        self.form_input = {
            'author': 'Test Author',
            'title': 'Test Title',
            'isbn': '1234567890123',
            'publication_date': '2023-01-01',

        }

    def test_create_book_url(self):
        self.assertEqual(self.url, '/create_book/')


    def test_get_create_book(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_book.html')
        form = response.context.get('form')
        self.assertTrue(isinstance(form, BookForm))  # Check if form is in context
        self.assertFalse(form.is_bound)  # Form should not be bound on GET request

    def test_post_with_valid_data(self):
        before_count = Book.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = Book.objects.count()
        self.assertEqual(after_count, before_count + 1) #book should be made so aftercount = beforecount +1
        expected_redirect_url = reverse('list_books')  # Assuming there's a view named 'list_books' to redirect to
        self.assertRedirects(response, expected_redirect_url, status_code=302, target_status_code=200)
        #302 means resource found and redirecting
        #target status code is the final landing page status code (i.e processed successfully)
        #200 means ok


    def test_post_with_invalid_data(self):
        self.form_input['author'] = ''  # Invalid as author is required
        before_count = Book.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = Book.objects.count()
        self.assertEqual(after_count, before_count)  # No new book should be created
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_book.html')
        form = response.context.get('form')
        self.assertTrue(isinstance(form, BookForm))  # Check if form is in context
        self.assertTrue(form.is_bound)  # Form should not be bound on GET request

    def test_book_with_non_unique_isbn(self):
        # First, create a book with a specific ISBN
        Book.objects.create(
            author='Existing Author',
            title='Existing Title',
            isbn='1234567890123',
            publication_date='2020-01-01'
        )
        # Now, try to create another book with the same ISBN
        before_count = Book.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = Book.objects.count()
        self.assertEqual(after_count, before_count)  # No new book should be created
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_book.html')
        form = response.context.get('form')
        self.assertTrue(isinstance(form, BookForm))  # Check if form is in context
        self.assertTrue(form.is_bound)  # Form should be bound
        self.assertIn('isbn', form.errors)  # There should be an error for the ISBN field