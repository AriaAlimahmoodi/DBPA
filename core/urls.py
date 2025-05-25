from django.urls import path
from .views import home, missions, ads
from django.contrib.auth.decorators import login_required
from core import views

urlpatterns = [
    path('', views.home,home, name='home'),  # صفحه اصلی (می‌تواند عمومی باشد)

    path('missions/', login_required(missions), name='missions'),  # فقط کاربر وارد شده
    path('ads/', login_required(ads), name='ads'),                 # فقط کاربر وارد شده
    path('missions/', views.missions, name='missions'),
    path('', views.home, name='home'),
    path('news/', views.news, name='news'),
    path('missions/', views.missions, name='missions'),
    path('ads/', views.ads, name='ads'),
]
