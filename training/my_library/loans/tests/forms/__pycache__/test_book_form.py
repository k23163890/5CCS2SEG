from django.test import TestCase
from django import forms
from loans.forms import BookForm
from loans.models import Book

import datetime


class BookFormTests(TestCase):


    def setUp(self):
        self.form_input = {
            'author': 'John Doe',
            'title': 'Sample Book',
            'isbn': '1234567890123',
            'publication_date': '2023-10-01',
        }

    def test_form_has_necessary_fields(self):
        form = BookForm()
        self.assertIn('author', form.fields)
        self.assertIn('title', form.fields)
        self.assertIn('isbn', form.fields)
        self.assertIn('publication_date', form.fields)
        publication_date_field = form.fields['publication_date']
        self.assertTrue(isinstance(publication_date_field, forms.DateField))


    def test_valid_form(self):
        form = BookForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_blank_author_is_invalid(self):
        self.form_input['author'] = ''
        form = BookForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertIn('author', form.errors)

    
    def test_publication_date_in_future_is_invalid(self):
        future_date = datetime.date.today() + datetime.timedelta(days=10)
        self.form_input['publication_date'] = future_date.isoformat()
        form = BookForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertIn('publication_date', form.errors)

    def test_isbn_too_long_is_invalid(self):
        self.form_input['isbn'] = '12345678901234'  # 14 characters
        form = BookForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertIn('isbn', form.errors)

    def test_isbn_too_short_is_invalid(self):
        self.form_input['isbn'] = '123456789012'  # 12 characters
        form = BookForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertIn('isbn', form.errors)

    def test_form_saves_correctly(self):
        form = BookForm(data=self.form_input)
        before_count = Book.objects.count()
        form.save()
        after_count = Book.objects.count()
        self.assertEqual(after_count, before_count + 1)
        new_book = Book.objects.get(isbn=self.form_input['isbn'])
        self.assertEqual(new_book.author, self.form_input['author'])
        self.assertEqual(new_book.title, self.form_input['title'])
        self.assertEqual(new_book.publication_date.isoformat(), self.form_input['publication_date'])


    #Test that a valid form can be saved and saving is equivalent to creating a new Book object in the database
    def test_valid_from_can_be_saved(self):
        form = BookForm(data=self.form_input)
        before_count = Book.objects.count()
        forms.save()
        after_count = Book.objects.count()
        self.assertEqual(after_count, before_count + 1)