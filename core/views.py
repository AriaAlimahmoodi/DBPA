from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.views.generic import TemplateView
from .models import Mission, Customer, NewsCards, MercenaryProfile, MercenaryUser
from .forms import MercenaryRegisterForm, CustomerRegisterForm
import json
import requests
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST
from .serializers import MercenaryProfileSerializer
from rest_framework import viewsets, permissions
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomerForm
# صفحه اصلی با اخبار
def home(request):
    news_cards_qs = NewsCards.objects.filter(enabled=True).order_by('-created_at')
    news_cards = list(news_cards_qs.values('site_name', 'description', 'image_url', 'site_url'))
    return render(request, 'core/home.html', {'news_cards_json': json.dumps(news_cards)})


# لیست مأموریت‌ها
def missions(request):
    missions = Mission.objects.all()
    return render(request, 'core/missions.html', {'missions': missions})


# ورود ادمین با AJAX
@csrf_exempt
def admin_login_ajax(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = authenticate(request, username=data.get('username'), password=data.get('password'))
        if user and user.is_staff:
            login(request, user)
            return JsonResponse({'success': True, 'redirect_url': '/admin/'})
        return JsonResponse({'success': False, 'message': 'نام کاربری یا رمز عبور نادرست است'})
    return JsonResponse({'success': False, 'message': 'درخواست نامعتبر'})


# ورود مزدور و مشتری با AJAX
@csrf_exempt
def login_user_ajax(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = authenticate(request, username=data.get('username'), password=data.get('password'))
        if user:
            login(request, user)
            try:
                MercenaryProfile.objects.get(user=user)
                return JsonResponse({'success': True, 'redirect_url': '/mercenary/dashboard/'})
            except MercenaryProfile.DoesNotExist:
                pass
            try:
                Customer.objects.get(user=user)
                return JsonResponse({'success': True, 'redirect_url': '/customer/dashboard/'})
            except Customer.DoesNotExist:
                pass
            return JsonResponse({'success': False, 'message': 'نوع کاربر مشخص نیست.'})
        return JsonResponse({'success': False, 'message': 'نام کاربری یا رمز عبور اشتباه است.'})
    return JsonResponse({'success': False, 'message': 'درخواست نامعتبر است.'})


# ثبت‌نام مزدور با AJAX (کاربر + پروفایل)
@csrf_exempt
def register_mercenary_ajax(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")
        if User.objects.filter(username=username).exists():
            return JsonResponse({"success": False, "message": "نام کاربری تکراری است."}, status=400)
        user = User.objects.create_user(username=username, password=password)
        MercenaryProfile.objects.create(
            user=user,
            name=data.get("name"),
            military_specialty=data.get("military_specialty"),
            military_rank=data.get("military_rank"),
            battalion=data.get("battalion"),
            nationality=data.get("nationality"),
            age=data.get("age"),
            height=data.get("height"),
            weight=data.get("weight"),
            about=data.get("about"),
        )
        login(request, user)
        return JsonResponse({"success": True, "message": "مزدور ثبت شد.", "redirect_url": "/mercenary/dashboard/"}, status=201)
    return JsonResponse({"success": False, "message": "روش ارسال نادرست است."}, status=400)


# ثبت‌نام مشتری با AJAX (کاربر + پروفایل)
@csrf_exempt
def register_customer_ajax(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")
        if User.objects.filter(username=username).exists():
            return JsonResponse({"success": False, "message": "نام کاربری تکراری است."}, status=400)
        user = User.objects.create_user(username=username, password=password)
        Customer.objects.create(user=user, alias=data.get("alias"))
        login(request, user)
        return JsonResponse({"success": True, "message": "مشتری ثبت شد.", "redirect_url": "/customer/dashboard/"}, status=201)
    return JsonResponse({"success": False, "message": "روش ارسال نادرست است."}, status=400)


# داشبورد مزدور
@login_required
def mercenary_dashboard(request):
    profile = get_object_or_404(MercenaryProfile, user=request.user)
    if not profile.is_approved:
        messages.warning(request, "پروفایل شما هنوز تایید نشده است.")
        return redirect('activate_profile')
    return render(request, 'core/mercenary_dashboard.html', {'profile': profile})


# داشبورد مشتری
@login_required
def customer_dashboard(request):
    profile = get_object_or_404(Customer, user=request.user)
    return render(request, 'core/customer_dashboard.html', {'profile': profile})


# ویرایش پروفایل مزدور
@login_required
def edit_profile_mercenary(request):
    profile = get_object_or_404(MercenaryProfile, user=request.user)
    if request.method == 'POST':
        for field in ['name', 'military_specialty', 'military_rank', 'battalion', 'nationality', 'age', 'height', 'weight', 'about']:
            setattr(profile, field, request.POST.get(field))
        profile.save()
        return redirect('/mercenary/dashboard/')
    return render(request, 'core/edit_mercenary.html', {'profile': profile})

@login_required
def edit_profile_mercenary(request):
    profile = get_object_or_404(MercenaryProfile, user=request.user)
    if request.method == 'POST':
        form = MercenaryRegisterForm(request.POST, instance=request.user)
        if form.is_valid():
            # چون فرم ما UserCreationForm است، باید فقط پروفایل رو جداگانه ذخیره کنیم:
            data = form.cleaned_data
            profile.name = data['name']
            profile.military_specialty = data['military_specialty']
            profile.military_rank = data['military_rank']
            profile.battalion = data['battalion']
            profile.nationality = data['nationality']
            profile.age = data['age']
            profile.height = data['height']
            profile.weight = data['weight']
            profile.about = data['about']
            profile.save()
            messages.success(request, 'پروفایل شما با موفقیت ویرایش شد.')
            return redirect('mercenary_dashboard')
    else:
        initial = {
            'name': profile.name,
            'military_specialty': profile.military_specialty,
            'military_rank': profile.military_rank,
            'battalion': profile.battalion,
            'nationality': profile.nationality,
            'age': profile.age,
            'height': profile.height,
            'weight': profile.weight,
            'about': profile.about,
        }
        form = MercenaryRegisterForm(initial=initial)
    return render(request, 'core/edit_mercenary.html', {'form': form})


# ویرایش پروفایل مشتری
@login_required
def edit_profile_customer(request):
    profile = get_object_or_404(Customer, user=request.user)
    if request.method == 'POST':
        profile.alias = request.POST.get('alias')
        profile.save()
        return redirect('/customer/dashboard/')
    return render(request, 'core/edit_customer.html', {'profile': profile})


# حذف پروفایل مزدور (برای کاربر خودش)
@login_required
@require_POST
def delete_profile(request):
    profile = get_object_or_404(MercenaryProfile, user=request.user)
    profile.delete()
    return JsonResponse({'success': True})


# لیست مزدورها (تایید شده)
def mercenaries(request):
    mercs = MercenaryProfile.objects.filter(is_approved=True)
    return render(request, 'core/mercenaries.html', {'mercenaries': mercs})


# تایید مزدور توسط ادمین
@staff_member_required
@require_POST
def approve_mercenary(request, mercenary_id):
    merc = get_object_or_404(MercenaryProfile, id=mercenary_id)
    merc.is_approved = True
    merc.save()
    messages.success(request, f"مزدور {merc.name} تایید شد.")
    return redirect('mercenaries')


# API کارت‌های خبری داخلی
def news_cards_api(request):
    cards = NewsCards.objects.order_by('-created_at')
    data = [
        {
            "title": card.site_name,
            "description": card.description,
            "image_url": card.image_url,
            "site_url": card.site_url,
        }
        for card in cards
    ]
    return JsonResponse(data, safe=False)


# API خبر از منابع خارجی
def external_news_api(request):
    cards = []
    sources = NewsCards.objects.filter(enabled=True)
    for source in sources:
        try:
            response = requests.get(source.api_url, timeout=5)
            if response.status_code == 200:
                news_list = response.json().get('articles', [])
                for news in news_list[:1]:
                    cards.append({
                        'title': news.get('title', 'بدون عنوان'),
                        'description': news.get('description', 'بدون توضیح'),
                        'image_url': news.get('urlToImage', ''),
                        'site_name': source.site_name,
                        'site_url': news.get('url', '#')
                    })
        except Exception:
            continue
    return JsonResponse(cards, safe=False)


# کلاس صفحه اصلی با context
class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cards = NewsCards.objects.filter(enabled=True).order_by('-created_at')
        context['news_cards'] = json.dumps([{
            "site_name": card.site_name,
            "image_url": card.image_url,
            "site_url": card.site_url,
            "description": card.description,
        } for card in cards], ensure_ascii=False)
        return context


# API ViewSet برای مزدور (فقط مالک)
class IsOwnerOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class MercenaryProfileViewSet(viewsets.ModelViewSet):
    serializer_class = MercenaryProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOnly]

    def get_queryset(self):
        return MercenaryProfile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# نمایش جزئیات مزدور
def mercenary_detail(request, id):
    mercenary = get_object_or_404(MercenaryProfile, id=id, is_approved=True)
    return render(request, 'core/mercenary_detail.html', {'mercenary': mercenary})


# صفحه فعال‌سازی پروفایل (مثلا بعد ثبت‌نام و منتظر تایید)
@login_required
def activate_profile(request):
    return render(request, 'core/activate_profile.html')


# نمایش فرم ویرایش پروفایل
@login_required
def profile_edit(request):
    user = request.user
    if hasattr(user, 'mercenaryprofile'):
        return edit_profile_mercenary(request)
    elif hasattr(user, 'customer'):
        return edit_profile_customer(request)
    else:
        messages.error(request, "پروفایلی برای ویرایش وجود ندارد.")
        return redirect('home')

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # تشخیص نوع کاربر و ریدایرکت
            if hasattr(user, 'mercenaryprofile'):
                return redirect('mercenary_dashboard')
            elif hasattr(user, 'customer'):
                return redirect('customer_dashboard')
            elif user.is_staff:
                return redirect('/admin/')
            else:
                messages.error(request, 'نوع کاربر مشخص نیست.')
                return redirect('login')
        else:
            messages.error(request, 'نام کاربری یا رمز عبور اشتباه است.')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})


@csrf_exempt
def customer_create_view(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
            return JsonResponse({'success': True, 'message': 'مشتری با موفقیت ثبت شد.', 'alias': customer.alias})
        return JsonResponse({'success': False, 'errors': form.errors})
    form = CustomerForm()
    return render(request, 'core/customer_form.html', {'form': form})


@csrf_exempt
def customer_update_view(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'اطلاعات مشتری بروزرسانی شد.'})
        return JsonResponse({'success': False, 'errors': form.errors})
    form = CustomerForm(instance=customer)
    return render(request, 'core/customer_form.html', {'form': form, 'customer': customer})
