from audioop import reverse

from django.contrib.auth.models import AbstractUser
from django.db import models

class Category(models.Model):
    name = models.CharField()

    def __str__(self):
        return self.name

class Status(models.Model):
    name = models.CharField()

class Application(models.Model):
    name = models.CharField(help_text='Название заявки')
    description = models.TextField(help_text='Описание заявки')
    category = models.OneToOneField(Category, on_delete=models.CASCADE, help_text='Выберете категорию заявки')
    photo = models.ImageField(help_text='Прикрепите фотографию')

    LOAN_STATUS = (
        ('new', 'new post'),
        ('accept', 'accepted for work'),
        ('done', 'done'),
    )
    status = models.OneToOneField(Status, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('application_detail', args=[str(self.pk)])

class Consumer(AbstractUser):
    first_name = models.CharField(help_text="Введите свое имя") #только кириллические буквы, дефис и пробелы;
    last_name = models.CharField(help_text="Введите свое имя")
    patronymic = models.CharField(help_text="Введите свое имя")
    login = models.CharField(help_text="Введите свое имя") #только латиница и дефис, уникальный;
    email = models.CharField(help_text="Введите почту") #валидный формат email-адрес;
    password = models.CharField(help_text="Введите пароль")

