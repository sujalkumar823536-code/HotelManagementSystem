from django.shortcuts import render,HttpResponse, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout ,authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from home.models import Signin ,Test
from datetime import datetime
from django.http import JsonResponse

# Create your views here.
def index(request):
    return render(request,"index.html")

def test(request):
    if request.method =="POST":
        location = request.POST.get('location')
        checkin = request.POST.get('checkin')
        checkout = request.POST.get('checkout')
        guest = request.POST.get('guest')
    
        if not location or not guest:
            messages.error(request, "All fields are required!")
            return redirect('test')
        
        test = Test(
            location=location,
            checkin=checkin,
            checkout=checkout,
            guest=guest
        )
        test.save()

        return redirect(f'/booking?location={location}&checkin={checkin}&checkout={checkout}')

    return render(request,"test.html")
    
def payment(request):
    location = request.GET.get('location')
    checkin = request.GET.get('checkin')
    checkout = request.GET.get('checkout')
    hotel = request.GET.get('hotel')

    try:
        price = int(request.GET.get('price', 0))
    except:
        price = 0

    days = 0
    total = 0
    if checkin and checkout and checkin != "None" and checkout != "None":
        from datetime import datetime

        try:
            d1 = datetime.strptime(checkin, "%Y-%m-%d")
            d2 = datetime.strptime(checkout, "%Y-%m-%d")

            days = (d2 - d1).days

            if days < 0:
                days = 0

            total = days * price

        except ValueError:
            days = 0
            total = 0

    return render(request, "payment.html", {
        'location': location,
        'checkin': checkin,
        'checkout': checkout,
        'hotel': hotel,
        'price': price,
        'days': days,
        'total': total
    })

def booking(request):
    location = request.GET.get('location')
    checkin = request.GET.get('checkin')
    checkout = request.GET.get('checkout')

    return render(request, "booking.html", {
        'location': location,
        'checkin': checkin,
        'checkout': checkout
    })

def user_signin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not username or not email or not password1 or not password2:
            messages.error(request, "All fields are required!")
            return redirect('signin')

        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return redirect('signin')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('signin')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )
        user.save()

        messages.success(request, "Account created successfully!")
        return redirect('login')

    return render(request, "signin.html")

def user_login(request):
    if request.method=="POST":
        username = request.POST.get('username')
        password= request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("test")
        else:
            return render(request,'login.html')
    
    return render(request,"login.html")

def user_logout(request):
    logout(request)
    return redirect("home")

def confirm_booking(request):
    if request.method == "POST":
        location = request.POST.get('location')
        hotel = request.POST.get('hotel')
        total = request.POST.get('total')

        return JsonResponse({
            "status": "success"
        })

    return JsonResponse({"status": "error"})