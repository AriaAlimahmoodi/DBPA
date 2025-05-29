from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from . import views
from .views import MercenaryProfileViewSet, home, news_cards_api
from .views import customer_create_view, customer_update_view, customer_register_view
router = DefaultRouter()
router.register('profile', MercenaryProfileViewSet, basename='profile')

urlpatterns = [
    # API routes
    path('api/', include(router.urls)),

    # صفحه اصلی سایت
    path('', home, name='home'),

    # Admin login (ajax)
    path('admin/login/ajax/', views.admin_login_ajax, name='admin_login_ajax'),

    # Missions
    path('missions/', views.missions, name='missions'),

    # Auth
    path('login/', views.login_user, name='login'),  # نمایش فرم لاگین
    path('login/ajax/', views.login_user_ajax, name='login_user_ajax'),  # ajax لاگین مزدور و مشتری
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

    # ثبت نام
    path('register/mercenary/', views.register_mercenary, name='register_mercenary'),
    path('customer/register/', customer_register_view, name='customer_register'),  # اگه لازم باشه
    path('customer/edit/<int:pk>/', customer_update_view, name='customer_edit'), 
    # Dashboards
    path('dashboard/mercenary/', views.mercenary_dashboard, name='mercenary_dashboard'),
    path('dashboard/customer/', views.customer_dashboard, name='customer_dashboard'),

    # عملیات مزدور
    path('mercenaries/', views.mercenaries, name='mercenaries'),
    path('mercenary/approve/<int:mercenary_id>/', views.approve_mercenary, name='approve_mercenary'),
    path('mercenary/delete-profile/', views.delete_profile, name='delete_profile'),
    path('mercenary/add/', views.mercenary_add, name='mercenary_add'),  # اگه استفاده میشه

    # ویرایش پروفایل مزدور و مشتری (یکسان)
    path('profile/edit/', views.profile_edit, name='profile_edit'),

    # فعال سازی پروفایل
    path('activate-profile/', views.activate_profile, name='activate_profile'),

    # APIهای اضافی
    path('api/news-cards/', news_cards_api, name='news_cards_api'),
    path('api/external-news/', views.external_news_api, name='external-news'),

    # نمایش جزئیات مزدور
    path('mercenary/<int:id>/', views.mercenary_detail, name='mercenary_detail'),
]

