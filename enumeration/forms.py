from cProfile import label

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Consumer


class RegistrationForm(UserCreationForm):
    class Meta:
        model = Consumer
        fields =['first_name', 'last_name', 'email', 'username']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'patronymic': 'Отчество',
            'email': 'Почта',
            'username': 'Логин',
        }
    #def validate_login(self, user):




    # first_name = models.CharField(help_text="Введите свое имя") #только кириллические буквы, дефис и пробелы;
    # last_name = models.CharField(help_text="Введите свою фамилию")
    # patronymic = models.CharField(help_text="Введите свое отчество")
    # login = models.CharField(help_text="Придумайте логин") #только латиница и дефис, уникальный;
    # email = models.CharField(help_text="Введите почту") #валидный формат email-адрес;