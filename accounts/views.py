from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            request.session['user_id'] = user.id
            return redirect('dashboard')
        else:
            return render(request, 'accounts/login.html', {'error': 'Invalid credentials'})
    return render(request, 'accounts/login.html')

def logout_view(request):
    request.session.flush()
    return redirect('login')

def dashboard_view(request):
    return render(request, 'accounts/dashboard.html')