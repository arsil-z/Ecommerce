from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from .models import *
from .utils import cookieCart, cartData, guestOrder
# from django.views.decorators.csrf import csrf_exempt
# Create your views here.


def store(request):

	data = cartData(request)
	cartItems = data['cartItems']

	products = Product.objects.all()
	context = {'products': products, 'cartItems': cartItems}
	return render(request, 'store/store.html', context)


def cart(request):

	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items': items, 'order': order, 'cartItems': cartItems}
	return render(request, 'store/cart.html', context)

def checkout(request):

	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

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

# @csrf_exempt
def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)
	print('body', request.body)
	print('id', transaction_id)
	print('data', data)
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)

	else:
		customer, order = guestOrder(request, data)
		print(customer)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id
	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping:
		ShippingAddress.objects.create(
			customer=customer, order=order,
			address=data['shipping']['address'],
			city=data['shipping']['city'],
			state=data['shipping']['state'],
			zipcode=data['shipping']['zipcode'])

	return JsonResponse('Payment Completed', safe=False)

#
# def processOrder(request):
# 	transaction_id = datetime.datetime.now().timestamp()
# 	data = json.loads(request.body)
#
# 	if request.user.is_authenticated:
# 		customer = request.user.customer
# 		order, created = Order.objects.get_or_create(customer=customer, complete=False)
# 	else:
# 		customer, order = guestOrder(request, data)
#
# 	total = float(data['form']['total'])
# 	order.transaction_id = transaction_id
#
# 	if total == order.get_cart_total:
# 		order.complete = True
# 	order.save()
#
# 	if order.shipping == True:
# 		ShippingAddress.objects.create(
# 		customer=customer,
# 		order=order,
# 		address=data['shipping']['address'],
# 		city=data['shipping']['city'],
# 		state=data['shipping']['state'],
# 		zipcode=data['shipping']['zipcode'],
# 		)
#
# 	return JsonResponse('Payment submitted..', safe=False)
#
