from lib2to3.fixes.fix_input import context

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from service.asgi import application
from .forms import RegistrationForm, ApplicationForm, ApplicationUpdateStatus, CategoryForm
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from enumeration.models import Application, Category
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy


def index(request):
    cards = Application.objects.filter(status__exact='d').order_by('date')[:4]
    counter = Application.objects.filter(status = 'a').count()
    context = {
        'cards': cards,
        'counter': counter
    }
    return render(request, 'index.html', context=context)



def consumer_login(request):
    if request.method == 'POST':
        form =  RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        form = RegistrationForm()

    context = {'form': form}

    return render(request, 'registration/registration.html', context)


class MyApplicationList(LoginRequiredMixin, generic.ListView):
    model = Application # application_list.html
    template_name = 'enumeration/my_applications.html'
    context_object_name = 'my_application'
    check = [False, False, False]
    filter = 0

    def get_queryset(self):

        if 'new' in self.request.GET and self.check[0] == False:
            self.check[0] = True
            self.check[1] = False
            self.check[2] = False

            return ({
                'check0': self.check[0],
                'check1': self.check[1],
                'check2': self.check[2],
                'application': Application.objects.filter(author=self.request.user, status='n').order_by('name')
            })

        if 'progress' in self.request.GET and self.check[1] == False:
            self.check[1] = True
            self.check[0] = False
            self.check[2] = False

            return ({
                'check0': self.check[0],
                'check1': self.check[1],
                'check2': self.check[2],
                'application': Application.objects.filter(author=self.request.user, status='a').order_by('name')

            })

        if 'done' in self.request.GET and self.check[2] == False:
            self.check[2] = True
            self.check[0] = False
            self.check[1] = False

            return ({
                'check0': self.check[0],
                'check1': self.check[1],
                'check2': self.check[2],
                'application': Application.objects.filter(author=self.request.user, status='d').order_by('name')
            })
        else:
            self.check[0] = False
            self.check[1] = False
            self.check[2] = False

            return ({
                'check0': self.check[0],
                'check1': self.check[1],
                'check2': self.check[2],
                'application': Application.objects.filter(author=self.request.user).order_by('name')
            })




class ApplicationAdd(LoginRequiredMixin, generic.edit.CreateView):
    model = Application
    form_class = ApplicationForm

    def form_valid(self, form):
        user = self.request.user
        app = form.save(commit=False)
        app.author = user
        app.save()
        return redirect('my_applications')

class ApplicationDelete(LoginRequiredMixin, generic.edit.DeleteView):
    model = Application
    success_url = reverse_lazy('my_applications')

    def form_valid(self, form):
        try:
            app = self.object
            if not(app.status == 'd' or app.status == 'a'):
                self.object.delete()
                return HttpResponseRedirect(reverse('my_applications'))
            else:
                return HttpResponseRedirect(reverse('my_applications'))

        except Exception as e:
            return HttpResponseRedirect(
                reverse('application-delete', kwargs={'pk': self.object.pk})
            )


class CategoryList(LoginRequiredMixin, generic.ListView):
    model = Category
    template_name = 'enumeration/category_list.html'
    context_object_name = 'category_list'

class CategoryDelete(LoginRequiredMixin, generic.edit.DeleteView):
    model = Category
    success_url = reverse_lazy('category_list')
    def form_valid(self, form):
        try:
            self.object.delete()
            return HttpResponseRedirect(reverse('category_list'))
        except Exception as e:
            return HttpResponseRedirect(
                reverse('category_list', kwargs={'pk': self.object.pk})
            )

class CategoryAdd(LoginRequiredMixin, generic.edit.CreateView):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('category_list')


class StatusUpdate(LoginRequiredMixin, generic.edit.UpdateView):
    model = Application
    form_class = ApplicationUpdateStatus
    context_object_name = 'form'
    template_name = 'enumeration/status_form.html'
    success_url = reverse_lazy('application_list')

    def form_valid(self, form):
        application = self.object
        status = form.cleaned_data['status']

        if status == 'a':
            application.status = 'a'
            application.comment = form.cleaned_data.get('comment', '')
            application.save()

        elif status == 'd':
            application.status = 'd'
            application.new_photo = form.cleaned_data.get('new_photo')
            application.save()

        return redirect(self.success_url)




class AllApplicationList(LoginRequiredMixin, generic.ListView):
    model = Application
    template_name = 'enumeration/all_applications.html'
    context_object_name = 'application_list'

