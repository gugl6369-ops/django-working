import re
from cProfile import label
from django.core.validators import validate_email
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Consumer, Application

class ApplicationForm(forms.ModelForm):
    photo = forms.ImageField(label=_('Photo'), required=True)
    class Meta:
        model = Application
        fields = ['name', 'description', 'category', 'photo']
        labels = {
            'name': 'Название',
            'description': 'Описание',
            'category': 'Категория',
            'photo': 'Фото',
        }


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

        def clean_last_name(self):
            reg = re.compile(r'[A-яЁё\-\s]+')
            data = self.cleaned_data['last_name']
            if not re.fullmatch(reg, data):
                raise ValidationError(f'нельзя тут {data},  только кириллические буквы, дефис и пробелы')
            return data

        def clean_patronymic(self):
            reg = re.compile(r'[A-яЁё\-\s]+')
            data = self.cleaned_data['patronymic']
            if not re.fullmatch(reg, data):
                raise ValidationError(f'нельзя тут {data},  только кириллические буквы, дефис и пробелы')
            return data

        def clean_username(self):
            reg = re.compile(r'[a-zA-z\-]+')
            data = self.cleaned_data['username']
            if not re.fullmatch(reg, data):
                raise ValidationError(f'нельзя тут {data}, только латиница и дефис')
            return data

