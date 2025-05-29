from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, AdminProfile  # نام مدل‌ها را با مدل واقعی خودت جایگزین کن

# اگر از AbstractUser استفاده کردی، می‌توانی کلاس UserAdmin را سفارشی کنی:
@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('username',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('سطوح دسترسی', {'fields': ('is_staff', 'is_superuser', 'is_active')}),
        ('تاریخچه', {'fields': ('last_login', 'date_joined')}),
    )

# اگر پروفایلی برای ادمین داری:
@admin.register(AdminProfile)
class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'position', 'created_at')  # به دلخواه تغییر بده
    search_fields = ('user__username', 'position')
