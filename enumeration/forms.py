import re
from dataclasses import fields

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.template.context_processors import request
from django.utils.translation import gettext_lazy as _
from .models import Consumer, Application, Category


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

    def clean_photo(self):
        data = self.files['photo']
        file_size = data.size
        file = data.name
        allowed_extensions = ['jpg', 'jpeg', 'png', 'bmp']
        if not(file.split('.')[-1] in allowed_extensions):
            raise ValidationError(f'Не то расширение изображения, возможны только: {allowed_extensions}')
        if file_size > 2 * 1024 * 1024:
            raise ValidationError(f'Изображение весит {data.size/1024/1024}MB, а максимальный размер 2MБ ')
        return data


class RegistrationForm(UserCreationForm):
        class Meta:
            model = Consumer
            fields =['first_name', 'last_name', 'patronymic', 'email', 'username']
            labels = {
                'first_name': 'Имя',
                'last_name': 'Фамилия',
                'patronymic': 'Отчество',
                'email': 'Почта',
                'username': 'Логин',
            }

        def clean_first_name(self):
            reg = re.compile(r'[А-яЁё\-\s]+')
            data = self.cleaned_data['first_name']
            if not re.fullmatch(reg, data):
                raise ValidationError(f'нельзя тут {data},  только кириллические буквы, дефис и пробелы')
            return data

        def clean_last_name(self):
            reg = re.compile(r'[А-яЁё\-\s]+')
            data = self.cleaned_data['last_name']
            if not re.fullmatch(reg, data):
                raise ValidationError(f'нельзя тут {data},  только кириллические буквы, дефис и пробелы')
            return data

        def clean_patronymic(self):
            reg = re.compile(r'[А-яЁё\-\s]+')
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

class ApplicationUpdateStatus(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['status', 'comment']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']



class ApplicationUpdateStatus(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['status', 'comment', 'new_photo']
        labels = {
            'status': 'Статус',
            'comment': 'Комментарий',
            'new_photo': 'Готовое фото',
        }

    def clean(self):
        status = self.cleaned_data.get('status')
        comment = self.cleaned_data.get('comment')
        new_photo = self.cleaned_data.get('new_photo')

        if self.instance.status != 'n':
            raise ValidationError('Эта заявка уже обработана и не может быть изменена.')

        if status == 'a':
            if not comment or not comment.strip():
                raise ValidationError({
                    'comment': 'При принятии заявки необходимо указать комментарий.'
                })

        elif status == 'd':
            if not new_photo:
                raise ValidationError({
                    'new_photo': 'При отклонении заявки необходимо прикрепить готовое фото.'
                })

        else:
            raise ValidationError({
                'status': 'Выберите корректный статус заявки.'
            })

        return self.cleaned_data







