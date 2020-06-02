from django.contrib import admin
from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path('category/<category_id>', views.category, name='category'),
    path('product/<product_id>', views.product, name='product')
]