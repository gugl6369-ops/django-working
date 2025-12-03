from django.shortcuts import render
from .forms import RegistrationForm
from django.views import generic
from enumeration.models import Application
from django.http import HttpResponseRedirect
from django.urls import reverse

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



class MyApplicationList(generic.ListView):
    model = Application # application_list.html
    template_name = 'enumeration/my_applications.html'
    context_object_name = 'my_application'
    #paginate_by = 10

    def get_queryset(self):
        return (
            Application.objects.filter(author=self.request.user).order_by('name')
        )
