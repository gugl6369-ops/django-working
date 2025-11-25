from lib2to3.fixes.fix_input import context
from urllib import request

from django.shortcuts import render
from .models import Book, Author, BookInstance,Genre

def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_genres = Genre.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()
    num_djin = Book.objects.filter(title__icontains='djin').count()

    return render(
        request,
        'index.html',

        context={'num_books': num_books,'num_instances' : num_instances,
            'num_instances_available' : num_instances_available, 'num_authors' : num_authors,
            'num_genres' : num_genres, 'num_djin' : num_djin},
    )

