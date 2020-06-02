from django.shortcuts import render
from .models import ProductCategory, Product, ProductImage
from orders.models import ProductInBasket

def category(request, category_id):
    current_category = ProductCategory.objects.filter(id=category_id)
    product_categories = ProductCategory.objects.all()
    products_images = ProductImage.objects.filter(is_active=True, is_main=True, product__category=category_id)
    session_key = request.session.session_key
    products_in_basket = ProductInBasket.objects.filter(session_key=session_key)
    products_in_basket_count = products_in_basket.count()
    return render(request, 'category.html', locals())


def product(request, product_id):
    product_images = ProductImage.objects.filter(is_active=True, product=product_id, is_main=False)
    product_image_main = ProductImage.objects.get(is_active=True, is_main=True, product=product_id)
    product = Product.objects.get(id=product_id)
    product_categories = ProductCategory.objects.all()
    session_key = request.session.session_key
    products_in_basket = ProductInBasket.objects.filter(session_key=session_key)
    products_in_basket_count = products_in_basket.count()
    return render(request, 'product.html', locals())
