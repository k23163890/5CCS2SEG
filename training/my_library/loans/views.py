from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import random
from django.urls import reverse
from .forms import BookForm


SLOGAN_LIST = [
    "Empowering Your Financial Future",
    "Loans Made Simple",
    "Your Trusted Loan Partner",
    "Fast, Flexible, Reliable Loans",
    "Bringing Dreams Within Reach",
]

# Create your views here.
def welcome_view(request):
    return render(request, 'welcome.html')

def list_books(request):
    context = {'books': Book.objects.all()}
    return render(request, 'books.html', context)


def get_book(request, book_id, bar, foo):
    return HttpResponse(f"Details of book with ID: {book_id}, foo: {foo}, bar: {bar}")

def create_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            """author = form.cleaned_data['author']
            title = form.cleaned_data['title']
            isbn = form.cleaned_data['isbn']
            publication_date = form.cleaned_data['publication_date']
            book  = Book(author=author, title=title, isbn=isbn, publication_date=publication_date)"""

            try:
                form.save() #a lot of code saved due to using ModelForm
            except Exception as e:
                form.add_error(None, f"An error occurred while saving the book: {str(e)}")
                return render(request, 'create_book.html', {'form': form})
            else:
                path = reverse('list_books')
                return HttpResponseRedirect(path) #we never hardcode urls / paths
    
    else:
        form = BookForm()
    return render(request, 'create_book.html', {'form': form})