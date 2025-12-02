from django.shortcuts import render
from .forms import RegistrationForm
from django.views import generic
from enumeration.models import Application
from django.http import HttpResponseRedirect
from django.urls import reverse

def index(request):
    return render(request, 'index.html')


class ApplicationList(generic.ListView):
    model = Application
    template_name = 'application_list.html'
    context_object_name = 'application_list'
    paginate_by = 10

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
