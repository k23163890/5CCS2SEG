from django import forms
from loans.models import Book


"""class BookForm(forms.Form):
    author = forms.CharField(max_length=100, label='Author')
    title = forms.CharField(max_length=200, label='Title')
    isbn = forms.CharField(max_length=13, label='ISBN')
    publication_date = forms.DateField(label='Publication Date', widget=forms.SelectDateWidget)"""


class BookForm(forms.ModelForm): #Subclass of form / has an autosave fucntion to the database
    class Meta:
        model = Book
        fields = ['author', 'title', 'isbn', 'publication_date']


