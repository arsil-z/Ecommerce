from django.contrib import admin
from .models import *
# Register your models here.

admin.site.Register(Customer)
admin.site.Register(Product)
admin.site.Register(Order)
admin.site.Register(OrderItem)
admin.site.Register(ShippingAddress)

