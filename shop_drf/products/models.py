from django.db import models


class Category(models.Model):
    sub_category = models.ForeignKey('self',on_delete=models.CASCADE,related_name='scategory',blank=True,null=True)
    is_sub = models.BooleanField(default=False)
    name = models.CharField(max_length=150)
    slug = models.SlugField()

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='products')
    name = models.CharField(max_length=150)
    slug = models.SlugField()
    is_available = models.BooleanField(default=True)
    image = models.ImageField()
    price = models.IntegerField()
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name

