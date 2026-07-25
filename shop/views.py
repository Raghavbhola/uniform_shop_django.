from django.shortcuts import render

from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Customer, Purchase

# Create your views here.

def get_points(amount):
    if amount <= 100:
        return 20
    elif amount <= 200:
        return 45
    elif amount <= 500:
        return 100
    else:
        return 150

def home(request):
    return render(request, 'shop/home.html')

def register(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        if phone and len(phone) == 10:
            customer, created = Customer.objects.get_or_create(phone=phone)
            return JsonResponse({
                'success': True,
                'points': customer.points,
                'message': 'Register ho gaye!' if created else 'Welcome back!',
                'new': created
            })
        return JsonResponse({'success': False, 'message': 'Phone number galat hai!'})

def add_purchase(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        amount = float(request.POST.get('amount', 0))
        try:
            customer = Customer.objects.get(phone=phone)
            pts = get_points(amount)
            customer.points += pts
            customer.save()
            Purchase.objects.create(
                customer=customer,
                amount=amount,
                points_earned=pts
            )
            return JsonResponse({
                'success': True,
                'points_earned': pts,
                'total_points': customer.points,
                'message': f'₹{amount} ki purchase — {pts} points mile!'
            })
        except Customer.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Customer register nahi hai!'})