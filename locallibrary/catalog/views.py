from dataclasses import fields
from lib2to3.fixes.fix_input import context
from urllib import request
import datetime
from django.views import generic
from django.shortcuts import render

from .forms import RenewBookForm
from .models import Book, Author, BookInstance,Genre
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Author

def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_genres = Genre.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()
    num_djin = Book.objects.filter(title__icontains='djin').count()

    num_visits = request.session.get('num_visits', 0)
    num_visits += 1
    request.session['num_visits'] = num_visits

    context = {
            'num_books': num_books,
            'num_instances': num_instances,
            'num_instances_available': num_instances_available,
            'num_authors': num_authors,
            'num_genres': num_genres,
            'num_djin': num_djin,
            'num_visits': num_visits,
    }

    return render( request,'index.html', context=context)


class BookListView(generic.ListView):
    model = Book
    context_object_name = 'book_list'
    template_name = 'book_list.html'
    paginate_by = 2

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author
    context_object_name = 'author_list'
    template_name = 'author_list.html'

class AuthorDetailView(generic.DetailView):
    context_object_name_book = 'book_list'
    model = Author

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact='o')
            .order_by('due_back')
        )


class AllBooksByUserListView(PermissionRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_all.html'
    paginate_by = 10
    permission_required = 'can_mark_returned'

    def get_queryset(self):
        return (
            BookInstance.objects.order_by('due_back')
        )

@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renewBookLibrarian (request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    if request.method == 'POST':
        form = RenewBookForm(request.POST)

        if form.is_valid():
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            return HttpResponseRedirect(reverse('all-borrowed'))
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

        context = {
            'form': form,
            'book_instance': book_instance,
        }
    return render(request, 'catalog/book_renew_librarian.html', context)

class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death' : '11/11/2023'}
    permission_required = 'catalog.add_author'

class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    fields = '__all__'
    permission_required = 'catalog.change_author'

class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    permission_required = 'catalog.delete_author'

    def form_valid(self, form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.get_success_url)
        except Exception as e:
            return HttpResponseRedirect(
                reverse('author-delete', kwargs={'pk': self.object.pk})
            )


# class BookCreate(PermissionRequiredMixin, CreateView):
#     model = Book
#     fields = ['title', 'author', 'summary', "isbn", 'denre']
#     initial = {'summary' : 'это книга.....'}
#     permission_required = 'catalog.add_author'
