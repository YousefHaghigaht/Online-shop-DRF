from django.db import models
from accounts.models import User
from products.models import Product
from django.core.validators import MaxValueValidator,MinValueValidator


class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='orders')
    paid = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    discount = models.PositiveSmallIntegerField(null=True,blank=True)

    def __str__(self):
        return str(self.id)

    def get_total_price(self):
        total = sum(item.get_cost() for item in self.items.all())
        if self.discount:
            discount_price = int((self.discount / 100 ) * total)
            return total - discount_price
        return total


class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items')
    products = models.ForeignKey(Product,on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.PositiveSmallIntegerField()

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.quantity * self.price


class Coupon(models.Model):
    code = models.CharField(max_length=30)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    is_active = models.BooleanField()
    discount = models.PositiveSmallIntegerField(validators=[MinValueValidator(10),MaxValueValidator(90)])

    def __str__(self):
        return self.code

