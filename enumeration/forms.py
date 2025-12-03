import re
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
    def clean_first_name(self):
        reg = re.compile(r'[A-яЁё\-\s]+')
        data = self.cleaned_data['first_name']
        if not re.fullmatch(reg, data):
            raise ValidationError(f'нельзя тут {data},  только кириллические буквы, дефис и пробелы')
        return data



    # first_name = models.CharField(help_text="Введите свое имя") #только кириллические буквы, дефис и пробелы;
    # last_name = models.CharField(help_text="Введите свою фамилию")
    # patronymic = models.CharField(help_text="Введите свое отчество")
    # login = models.CharField(help_text="Придумайте логин") #только латиница и дефис, уникальный;
    # email = models.CharField(help_text="Введите почту") #валидный формат email-адрес;