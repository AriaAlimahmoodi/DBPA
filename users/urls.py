from django.urls import path
from .views import register, CustomLoginView, profile, manage_users
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', register, name='register'),        # ثبت نام کاربر (باز)
    path('login/', CustomLoginView.as_view(), name='login'),  # لاگین (باز)
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),  # خروج (فقط کاربر وارد شده)
    path('profile/', profile, name='profile'),           # صفحه پروفایل (فقط کاربر وارد شده)
    path('manage/', manage_users, name='manage_users'),  # مدیریت کاربران (فقط ادمین)
]
