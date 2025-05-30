from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from . import views
from .views import approved_missions_view
from .views import (
    MercenaryProfileViewSet,
    home,
    news_cards_api,
    external_news_api,
    customer_register_view,
    customer_update_view,
    mercenary_dashboard,
    customer_dashboard,
)

router = DefaultRouter()
router.register('profile', MercenaryProfileViewSet, basename='profile')

urlpatterns = [
    # صفحه اصلی
    path('', home, name='home'),
    path('login/', views.custom_login, name='custom_login'),
    path('register/customer/', views.customer_register_view, name='register_customer'),
    path('mercenaries/', views.mercenaries, name='mercenaries'),

    # ------------------ AUTH ------------------
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('login/', views.login_view, name='login'),
    # ------------------ ADMIN ------------------
    path('admin/login/ajax/', views.admin_login_ajax, name='admin_login_ajax'),

    # ------------------ MERCENARY ------------------
    path('register/mercenary/', views.register_mercenary, name='register_mercenary'),
    path('login/mercenary/', views.login_mercenary, name='login_mercenary'),
    path('dashboard/mercenary/', mercenary_dashboard, name='mercenary_dashboard'),
    path('mercenary/profile/edit/', views.profile_edit, name='profile_edit'),
    path('mercenary/delete-profile/', views.delete_profile, name='delete_profile'),
    path('mercenary/activate/', views.activate_profile, name='activate_profile'),
    path('mercenary/<int:id>/', views.mercenary_detail, name='mercenary_detail'),
    path('mercenary/approve/<int:mercenary_id>/', views.approve_mercenary, name='approve_mercenary'),
    path('mercenary/add/', views.mercenary_add, name='mercenary_add'),
    path('mercenaries/add/', views.add_mercenary_ajax, name='add_mercenary_ajax'),
    path('api/mercenaries/', views.mercenary_list_json, name='mercenary_list_json'),
    path('mercenary/profile/', views.MercenaryProfile, name='mercenary_profile'),
    path('mercenaries/', views.mercenaries_list, name='mercenaries_list'),
    path('dashboard/mercenary/update/', views.update_mercenary_profile, name='update_mercenary_profile'),
    # ------------------ CUSTOMER ------------------
    path('customer/register/', customer_register_view, name='customer_register'),
    path('customer/login/', views.custom_login, name='login_customer'),
    path('dashboard/customer/', customer_dashboard, name='customer_dashboard'),
    path('customer/edit/<int:pk>/', customer_update_view, name='customer_edit'),
    path('customer/delete/', views.customer_delete, name='customer_delete'),

    # ------------------ COMMON / AJAX ------------------
    path('login/ajax/', views.login_user_ajax, name='login_user_ajax'),  # اگر هنوز استفاده می‌شود

    # ------------------ API ------------------
    path('api/', include(router.urls)),
    path('api/news-cards/', news_cards_api, name='news_cards_api'),
    path('api/external-news/', external_news_api, name='external-news'),

    # ------------------ MISSIONS ------------------
    path('mercenaries/', views.mercenaries, name='mercenaries'),
    path('missions/', approved_missions_view, name='missions'),
    path('missions/', views.mission_list_view, name='mission_list'),
    path('missions/reserve/<int:mission_id>/', views.reserve_mission, name='reserve_mission'),
]


