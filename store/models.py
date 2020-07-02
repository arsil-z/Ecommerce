from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Customer(models.Model):

    """ Using the Pre Built Django Model User and connecting it
        to OneToOneField, since each user can be assigned to only 
        one customer Model.
    """

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):

    """ Using digital as a BooleanField because if the product is 
        not digital then shipping process will be carried out.
    
    """

    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=True)
    # Image 
    def __str__(self):
        return self.name

class Order(models.Model):

    """ One customer can have multiple Orders so ForeignKey and when the customer 
        is deleted setting the value to NULL so that still the data is present about
        that order.
    """

    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length = 200)

    def __str__(self):
        return str(self.id)

class OrderItem(models.Model):

    """ Using both the Models Product to know which product is ordered
    and the order in which that product is present.

    """

    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)


class ShippingAddress(models.Model):

    """ Shipping address of each customer their can be multiple so using ForeignKey
        and for each non-digital order shipping address is must.
    """

    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    sate = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.address

