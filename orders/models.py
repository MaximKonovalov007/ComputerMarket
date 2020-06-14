from django.db import models
from products.models import Product
from django.db.models.signals import post_save
from django.contrib.auth.models import User

class Status(models.Model):
    name = models.CharField(max_length=24, blank=True, null=True, default=None)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "%s" % self.name

    class Meta:
        verbose_name = "Статус заказа"
        verbose_name_plural = "Статусы заказов"


class Order(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    customer_name = models.CharField(max_length=64, blank=True, null=True, default=None)
    customer_email = models.EmailField(blank=True, null=True, default=None)
    customer_phone = models.CharField(max_length=48, blank=True, null=True, default=None)
    customer_address = models.CharField(max_length=48, blank=True, null=True, default=None)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, default=1)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "Статус %s" % self.customer_name

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class ProductInOrder(models.Model):
    order = models.ForeignKey(Order, blank=True, null=True, default=None, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, blank=True, null=True, default=None, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)
    amount_per_item = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "%s" % self.product.name

    class Meta:
        verbose_name = "Товар в заказе"
        verbose_name_plural = "Товары в заказе"


class ProductInBasket(models.Model):
    session_key = models.CharField(max_length=128, blank=True, null=True, default=None)
    product = models.ForeignKey(Product, blank=True, null=True, default=None, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, blank=True, null=True, default=None)
    count = models.IntegerField(default=1)
    amount_per_item = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    product_total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "%s" % self.product.name

    class Meta:
        verbose_name = "Товар в корзине"
        verbose_name_plural = "Товары в корзине"

    def save(self, *args, **kwargs):
        price_per_item = self.product.price
        self.product_total_amount = price_per_item * int(self.count)
        super(ProductInBasket, self).save(*args, **kwargs)

    def product_in_order_post_save(sender, instance, created, **kwargs):
        order = instance.order
        all_products_in_order = ProductInOrder.objects.filter(order=order, is_active=True)

        order_total_price = 0
        for item in all_products_in_order:
            order_total_price += item.total_amount

        instance.order.total_amount = order_total_price
        instance.order.save(force_update=True)

    post_save.connect(product_in_order_post_save, sender=ProductInOrder)






