from django.shortcuts import render
from django.views import generic

from enumeration.models import Application


def index(request):
    return render(request, 'index.html')


class ApplicationList(generic.ListView):
    model = Application
    template_name = 'application_list.html'
    context_object_name = 'application_list'
    paginate_by = 10