from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import UserRegistrationForm
from django.contrib.auth.views import LoginView

# دکوراتور اختصاصی برای ادمین
def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and hasattr(request.user, 'role') and request.user.role.name == 'admin':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login')  # یا صفحه خطای دسترسی
    return wrapper

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'users/login.html'

@login_required
def profile(request):
    # صفحه پروفایل کاربر
    return render(request, 'users/profile.html')

@admin_required
def manage_users(request):
    # صفحه مدیریت کاربران و محتوا برای ادمین
    # لیست کاربران، حذف، اضافه و مدیریت سایت
    return render(request, 'users/manage_users.html')
