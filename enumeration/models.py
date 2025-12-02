from audioop import reverse

from django.contrib.auth.models import AbstractUser
from django.db import models


class Consumer(AbstractUser):
    first_name = models.CharField(help_text="Введите свое имя") #только кириллические буквы, дефис и пробелы;
    last_name = models.CharField(help_text="Введите свою фамилию")
    patronymic = models.CharField(help_text="Введите свое отчество")
    login = models.CharField(help_text="Придумайте логин") #только латиница и дефис, уникальный;
    email = models.CharField(help_text="Введите почту") #валидный формат email-адрес;



class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name



class Application(models.Model):
    name = models.CharField(help_text='Название заявки', max_length=255)
    description = models.TextField(help_text='Описание заявки')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, help_text='Выберете категорию заявки')
    photo = models.ImageField(help_text='Прикрепите фотографию', upload_to='photos/')

    LOAN_STATUS = (
        ('n', 'Новая'),
        ('a', 'Принято в работу'),
        ('d', 'Выполнено'),
    )
    status = models.CharField(choices=LOAN_STATUS, default='n',)

    class Meta:
        ordering = ['status']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('application_detail', args=[str(self.pk)])
