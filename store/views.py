from django.shortcuts import render
from django.http import JsonResponse
import json

from .models import *


# Create your views here.


def store(request):

	cartItems = getCartItems(request)

	products = Product.objects.all()
	context = {
		'products': products,
		'cartItems': cartItems
	}
	return render(request, 'store/store.html', context)


def cart(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(
			customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		items = []
		order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
		cartItems = order['get_cart_items']
	context = {'items': items, 'order': order, 'cartItems': cartItems}
	return render(request, 'store/cart.html', context)


def checkout(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(
			customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		items = []
		order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
		cartItems = order['get_cart_items']

	context = {'items': items, 'order': order, 'cartItems': cartItems}
	return render(request, 'store/checkout.html', context)


def updateItem(request):
	data = json.loads(request.body)  # request.body is the body passes in cart.js (eg. {'productId': '3', 'action':
	# 'add'} )
	productId = data['productId']
	action = data['action']

	print('ProductId: ', productId)
	print('Action: ', action)
	print('data', data)

	customer = request.user.customer  # Querying the logged in customer (as customer is inherited by User class)
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)  # get_or_create it returns the
	# order as a object as we use 'get' to get any object, if that object is not present it creates that object,
	# in the second argument it return boolean representing whether that object was created or not.

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)  # Since orderItemis connected
	# to both models.

	if action == 'add':
		orderItem.quantity += 1
	elif action == 'remove':
		orderItem.quantity -= 1

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)


def getCartItems(req):
	if req.user.is_authenticated:
		customer = req.user.customer
		order, created = Order.objects.get_or_create(
			customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		items = []
		order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
		cartItems = order['get_cart_items']

	return cartItems
