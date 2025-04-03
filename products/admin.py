from django.contrib import admin
from . import models

class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','gender', 'article_type', 'base_colour', 'product_display_name']

class WishlistAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product']

admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Wishlist, WishlistAdmin)