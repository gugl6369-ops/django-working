from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Application(models.Model):
    name = models.CharField(max_length=100, help_text='Название заявки')
    description = models.TextField(max_length=500, help_text='Описание заявки')
    category = models.OneToOneField(Category, help_text='Выберете категорию заявки')
    photo = models.ImageField(help_text='Прикрепите фотографию')
    status = models.OneToOneField(status)