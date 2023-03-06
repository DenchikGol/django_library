from django.shortcuts import render
from .models import Book, Author, BookInstance
from django.views import generic

def index(request):
    sum_books = Book.objects.all().count()
    sum_instance = BookInstance.objects.all().count()
    sum_available_books = BookInstance.objects.filter(status__exact="д").count()
    sum_authors = Author.objects.all().count()
    sum_visits = request.session.get('sum_visits', 0)
    request.session['sum_visits'] = sum_visits + 1

    context = {
        'sum_books': sum_books,
        'sum_instance': sum_instance,
        'sum_available_books': sum_available_books,
        'sum_authors': sum_authors,
        'sum_visits': sum_visits,
    }

    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    model = Book
    paginate_by = 10


class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10


class AuthorDetailView(generic.DetailView):
    model = Author
