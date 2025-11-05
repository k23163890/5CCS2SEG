from loans.models import Book
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
import datetime

class BookTestCase(TestCase):
    def setUp(self):
        authors = "Jane Austen"
        title = "Pride and Prejudice"
        isbn = "1112223334445"
        publication_date = datetime.date(1813, 1, 28)
        self.book = Book(
            author=authors,
            title=title,
            isbn=isbn,
            publication_date=publication_date
        )

    def test_valid_book_is_valid(self):
        try:
            self.book.full_clean()
        except ValidationError:
            self.fail("Valid book raised ValidationError")


    def test_blank_author_is_invalid(self):
        self.book.author = ''
        with self.assertRaises(ValidationError):
            self.book.full_clean()

    def test_book_with_overlong_author_is_invalid(self):
        self.book.author = 'A' * 101  # 101 characters
        with self.assertRaises(ValidationError):
            self.book.full_clean()

    def test_isbn_unique_constraint(self):
        self.book.save()
        duplicate_book = Book(
            author="Another Author",
            title="Another Title",
            isbn=self.book.isbn,  # Same ISBN
            publication_date=datetime.date(2000, 1, 1)
        )
        with self.assertRaises(ValidationError):
            duplicate_book.full_clean()


    def test_publication_date_cannot_be_in_future(self):
        self.book.publication_date = datetime.date.today() + datetime.timedelta(days=1)
        with self.assertRaises(ValidationError):
            self.book.full_clean()


    def test_book_saves_correctly(self):
        self.book.full_clean()  # Should not raise
        self.book.save()
        saved_book = Book.objects.get(id=self.book.id)
        self.assertEqual(saved_book.author, self.book.author)
        self.assertEqual(saved_book.title, self.book.title)
        self.assertEqual(saved_book.isbn, self.book.isbn)
        self.assertEqual(saved_book.publication_date, self.book.publication_date)

    
    def test_book_isbn_must_be_unique(self):
        self.book.save()
        another_book = Book(
            author="Different Author",
            title="Different Title",
            isbn=self.book.isbn,  # Duplicate ISBN
            publication_date=datetime.date(1999, 12, 31)
        )
        with self.assertRaises(IntegrityError):
            Book.objects.create(
                author=another_book.author,
                title=another_book.title,
                isbn=another_book.isbn,
                publication_date=another_book.publication_date
            )


    