from tabnanny import check
from unicodedata import category
from urllib import request

from django.shortcuts import render, redirect

from service.asgi import application
from .forms import RegistrationForm, ApplicationForm, ApplicationUpdateStatus
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from enumeration.models import Application
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy


def index(request):
    cards = Application.objects.filter(status__exact='d')
    context = {'cards': cards}
    return render(request, 'index.html', context=context)

class ApplicationList(generic.ListView):
    model = Application
    template_name = 'application_list.html'
    context_object_name = 'application_list'
   # paginate_by = 10

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
    check = 0
    filter = 0


    #paginate_by = 10
    def get_queryset(self):
        if 'new' in self.request.GET and not(self.check == 1):
            self.check = 1
            self.filter = Application.objects.filter(author=self.request.user, status='n').order_by('name')

        elif 'progress' in self.request.GET and self.check != 2:
            self.check = 2
            self.filter = Application.objects.filter(author=self.request.user, status='a').order_by('name')

        elif 'done' in self.request.GET and self.check != 3:
            self.check = 3
            self.filter = Application.objects.filter(author=self.request.user, status='d').order_by('name')


        else:
            self.check = 0
            self.filter = Application.objects.filter(author=self.request.user).order_by('name')

        return ({
            'check' : self.check,
            'application': self.filter
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




