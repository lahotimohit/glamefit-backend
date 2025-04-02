from django.contrib import admin
from . import models

class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','gender', 'article_type', 'base_colour', 'product_display_name']

admin.site.register(models.Product, ProductAdmin)