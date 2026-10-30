from django.shortcuts import render

from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Customer, Purchase
from django.contrib.auth.decorators import login_required
from urllib.parse import quote

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

# def add_purchase(request):
#     if request.method == 'POST':
#         phone = request.POST.get('phone')
#         amount = float(request.POST.get('amount', 0))
#         try:
#             customer = Customer.objects.get(phone=phone)
#             pts = get_points(amount)
#             customer.points += pts
#             customer.save()
#             Purchase.objects.create(
#                 customer=customer,
#                 amount=amount,
#                 points_earned=pts
#             )
#             return JsonResponse({
#                 'success': True,
#                 'points_earned': pts,
#                 'total_points': customer.points,
#                 'message': f'₹{amount} ki purchase — {pts} points mile!'
#             })
#         except Customer.DoesNotExist:
#             return JsonResponse({'success': False, 'message': 'Customer register nahi hai!'})
@login_required
def add_purchase(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        try:
            amount = float(request.POST.get('amount', 0))
        except ValueError:
            return JsonResponse({'success': False, 'message': 'Amount galat hai!'})
        if amount <= 0:
            return JsonResponse({'success': False, 'message': 'Amount 0 se zyada hona chahiye!'})
        try:
            customer = Customer.objects.get(phone=phone)
        except Customer.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Customer register nahi hai!'})
        pts = get_points(amount)
        customer.points += pts
        customer.save()
        Purchase.objects.create(customer=customer, amount=amount, points_earned=pts)
        remaining = max(1000 - customer.points, 0)
        msg = (
            f"🙏 Namaste! Thank you for visiting *Shree Krishan Uniform* 😊\n\n"
            f"🛍️ Aaj ki purchase (amount): *₹{amount:g}*\n"
            f"🎁 Points Earned today: *{pts}*\n"
            f"⭐ Total points: *{customer.points}*\n"
            f"🎯 Discount ke liye baaki: *{remaining}* points\n\n"
            f"Phir aaiyega! we'd love to see you again! 🏫👕"
        )    
        link = f"https://api.whatsapp.com/send?phone=91{customer.phone}&text={quote(msg, safe='')}"
        return JsonResponse({
            'success': True,
            'points_earned': pts,
            'total_points': customer.points,
            'message': f'₹{amount} ki purchase, {pts} points mile!',
            'whatsapp_link': link,
        })

@login_required
def staff(request):
    return render(request, 'shop/staff.html')    

@login_required
def search_customers(request):
    q = request.GET.get('q', '')
    customers = Customer.objects.filter(phone__startswith=q)[:8] if q else []
    return JsonResponse({'results': [{'phone': c.phone, 'points': c.points} for c in customers]})