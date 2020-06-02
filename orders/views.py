from django.shortcuts import render
from django.http import JsonResponse
from products.models import ProductCategory, ProductImage, Product
from .models import *


def home(request):
    product_categories = ProductCategory.objects.all()
    products_images = ProductImage.objects.filter(is_main=True)
    session_key = request.session.session_key
    products_in_basket = ProductInBasket.objects.filter(session_key=session_key)
    products_in_basket_count = products_in_basket.count()

    return render(request, 'home.html', locals())


def basket_adding(request):
    return_dict = {}
    session_key = request.session.session_key
    data = request.POST
    product_id = data.get("product_id")
    product = Product.objects.get(id=product_id)
    product_name = data.get("product_name")
    product_price = product.price
    number = request.POST['number']

    new_product, created = ProductInBasket.objects.get_or_create(session_key=session_key, product_id=product_id, name=product_name, amount_per_item=product_price, defaults={"count": number})

    if not created:
        new_product.count += int(number)
        new_product.save(force_update=True)

    products_in_basket = ProductInBasket.objects.filter(session_key=session_key)
    products_in_basket_count = products_in_basket.count()

    return_dict["products_in_basket_count"] = products_in_basket_count
    return_dict["products_in_basket"] = list()

    for item in products_in_basket:
        product_dict = dict()
        print(item)
        product_dict["id"] = item.id
        product_dict["name"] = item.name
        product_dict["price"] = item.amount_per_item
        product_dict["count"] = item.count
        product_dict["product_id"] = item.product.id
        product_dict["product_total_amount"] = item.product_total_amount
        return_dict["products_in_basket"].append(product_dict)

    return JsonResponse(return_dict)


def checkout(request):
    session_key = request.session.session_key
    products_in_basket = ProductInBasket.objects.filter(session_key=session_key)
    products_in_basket_count = products_in_basket.count()
    total_order_amount = 0
    for product_in_basket in products_in_basket:
        total_order_amount += product_in_basket.product_total_amount
    return render(request, 'checkout.html', locals())
