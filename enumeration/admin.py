from django.contrib import admin
from .models import Application, Consumer, Category

admin.site.register(Category)

@admin.register(Consumer)
class ConsumerAdmin(admin.ModelAdmin):
    model = Consumer

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    model = Application

