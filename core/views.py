# views.py
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse, HttpResponseForbidden
from .forms import MercenaryRegisterForm, CustomerRegisterForm, LoginForm
from .models import MercenaryProfile, Customer
from rest_framework import viewsets
from .serializers import MercenaryProfileSerializer
from .models import Mission
from django.contrib import messages
from django.http import JsonResponse
from .forms import MercenaryProfile
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
# صفحه اصلی
def home(request):
    return render(request, 'core/home.html')

# ---------------- MERCENARY ------------------
def register_mercenary(request):
    if request.method == 'POST':
        form = MercenaryRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'errors': form.errors}, status=400)
    return HttpResponseForbidden()

class MercenaryLoginView(View):
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, 
                                username=form.cleaned_data['username'], 
                                password=form.cleaned_data['password'])
            if user is not None and MercenaryProfile.objects.filter(user=user).exists():
                login(request, user)
                return JsonResponse({'status': 'success', 'redirect': '/dashboard/mercenary/'})
            return JsonResponse({'status': 'error', 'message': 'اطلاعات ورود نادرست یا حساب مزدور نیست'})
        return JsonResponse({'status': 'error', 'message': 'فرم نامعتبر است'})

@login_required
def mercenary_dashboard(request):
    profile, created = MercenaryProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = MercenaryProfile(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "پروفایل با موفقیت ذخیره شد. در انتظار تایید ادمین.")
            return redirect('mercenary_dashboard')
    else:
        form = MercenaryProfile(instance=profile)

    return render(request, 'dashboard/mercenary_dashboard.html', {
        'form': form,
        'profile': profile
    })@login_required
def profile_edit(request):
    profile = get_object_or_404(MercenaryProfile, user=request.user)
    if request.method == 'POST':
        for field in ['name', 'military_specialty', 'military_rank', 'battalion', 'nationality', 'age', 'height', 'weight', 'about']:
            setattr(profile, field, request.POST.get(field))
        profile.save()
        return redirect('mercenary_dashboard')
    return render(request, 'edit_profile.html', {'profile': profile})

@login_required
def delete_profile(request):
    MercenaryProfile.objects.filter(user=request.user).delete()
    request.user.delete()
    return redirect('home')

@login_required
def activate_profile(request):
    profile = get_object_or_404(MercenaryProfile, user=request.user)
    profile.is_active = True
    profile.save()
    return redirect('mercenary_dashboard')

def mercenary_detail(request, id):
    profile = get_object_or_404(MercenaryProfile, id=id, is_active=True)
    return render(request, 'mercenary_detail.html', {'profile': profile})

@staff_member_required
def approve_mercenary(request, mercenary_id):
    profile = get_object_or_404(MercenaryProfile, id=mercenary_id)
    profile.is_approved = True
    profile.save()
    return redirect('home')

# صفحه‌ی نمایش پروفایل‌های تأییدشده‌ی مزدوران
def mercenaries(request):
    profiles = MercenaryProfile.objects.filter(approved=True)
    return render(request, 'core/mercenaries.html', {'profiles': profiles})

@login_required
def add_mercenary_ajax(request):
    if not request.user.is_staff:
        return JsonResponse({'status': 'error', 'message': 'دسترسی غیرمجاز'})

    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('age')
        specialty = request.POST.get('specialty')
        experience = request.POST.get('experience')
        # ذخیره در مدل
        MercenaryProfile.objects.create(
            name=name, age=age, specialty=specialty, experience=experience
        )
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'درخواست نامعتبر'})

@login_required
def mercenary_add(request):
    if request.method == 'POST':
        form = MercenaryProfile(request.POST, request.FILES)
        if form.is_valid():
            mercenary = form.save(commit=False)
            mercenary.user = request.user
            mercenary.save()
            return redirect('mercenary_dashboard')
    else:
        form = MercenaryProfile()
    return render(request, 'mercenaries/add.html', {'form': form})
@login_required
def mercenary_list_json(request):
    if request.user.is_staff:
        mercenaries = MercenaryProfile.objects.all()
    else:
        mercenaries = MercenaryProfile.objects.filter(user=request.user)

    data = []
    for m in mercenaries:
        data.append({
            "id": m.id,
            "name": m.name,
            "image": m.image.url if m.image else "",
            "military_specialty": m.military_specialty,
            "military_rank": m.military_rank,
            "battalion": m.battalion,
            "nationality": m.nationality,
            "age": m.age,
            "height": m.height,
            "weight": m.weight,
            "about": m.about,
        })
    return JsonResponse({"mercenaries": data})

@csrf_exempt
@login_required
def mercenary_profile_view(request):
    if request.method == 'POST':
        try:
            profile, created = MercenaryProfile.objects.get_or_create(user=request.user)
            form = MercenaryProfile(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                return JsonResponse({'status': 'success', 'message': 'پروفایل ذخیره شد.'})
            else:
                return JsonResponse({'status': 'error', 'errors': form.errors})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'درخواست نامعتبر است.'})

def mercenaries_list(request):
    mercenaries = MercenaryProfile.objects.filter(is_approved=True)
    return render(request, 'mercenaries.html', {'mercenaries': mercenaries})

@login_required
def update_mercenary_profile(request):
    if request.method == 'POST':
        profile, _ = MercenaryProfile.objects.get_or_create(user=request.user)
        form = MercenaryProfile(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': '✅ پروفایل با موفقیت ذخیره شد.'})
        else:
            return JsonResponse({'success': False, 'message': '❌ لطفاً تمام فیلدها را به درستی پر کنید.'})
    return JsonResponse({'success': False, 'message': 'درخواست نامعتبر'})

# ---------------- CUSTOMER ------------------
def customer_register_view(request):
    if request.method == 'POST':
        form = CustomerRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'errors': form.errors}, status=400)
    return HttpResponseForbidden()

@csrf_exempt
def custom_login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return JsonResponse({'success': True, 'message': 'Login successful'})
            else:
                return JsonResponse({'success': False, 'message': 'Invalid credentials'}, status=401)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)

    # اگر متد POST نبود
    return JsonResponse({'error': 'Invalid request method'}, status=405)
@login_required
def customer_dashboard(request):
    customer = get_object_or_404(Customer, user=request.user)
    return render(request, 'dashboard_customer.html', {'customer': customer})

@login_required
def customer_update_view(request, pk):
    customer = get_object_or_404(Customer, pk=pk, user=request.user)
    if request.method == 'POST':
        customer.alias = request.POST.get('alias')
        customer.save()
        return redirect('customer_dashboard')
    return render(request, 'edit_customer.html', {'customer': customer})

@login_required
def customer_delete(request):
    Customer.objects.filter(user=request.user).delete()
    request.user.delete()
    return redirect('home')
@login_required
def reserve_mission(request, mission_id):
    mission = get_object_or_404(Mission, id=mission_id)

    try:
        mercenary = request.user.mercenaryprofile
    except:
        messages.error(request, "فقط مزدوران می‌توانند مأموریت رزرو کنند.")
        return redirect('mission_list')

    if mission.selected_mercenary:
        messages.error(request, "این مأموریت قبلاً رزرو شده است.")
    else:
        mission.selected_mercenary = mercenary
        mission.save()
        messages.success(request, "درخواست شما ثبت شد و منتظر تأیید است.")

    return redirect('mission_list')


# ---------------- API ------------------
from django.http import JsonResponse

def news_cards_api(request):
    return JsonResponse({'cards': []})

def external_news_api(request):
    return JsonResponse({'news': []})

# ---------------- DRF ------------------
class MercenaryProfileViewSet(viewsets.ModelViewSet):
    queryset = MercenaryProfile.objects.all()
    serializer_class = MercenaryProfileSerializer

def approved_missions_view(request):
    missions = Mission.objects.filter(is_customer_approved=True, is_admin_approved=True)
    return render(request, 'missions.html', {'missions': missions})

def admin_login_ajax(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user is not None and user.is_staff:
            login(request, user)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'message': 'نام کاربری یا رمز عبور نادرست است'})
    
    return JsonResponse({'success': False, 'message': 'درخواست نامعتبر'})

def login_user_ajax(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'نام کاربری یا رمز عبور اشتباه است'})

    return JsonResponse({'status': 'error', 'message': 'درخواست نامعتبر'})

def missions(request):
    mission_list = Mission.objects.filter(admin_approved=True, customer_approved=True)
    return render(request, 'missions.html', {'missions': mission_list})

def mission_list_view(request):
    missions = Mission.objects.filter(admin_approved=True, customer_approved=True)
    return render(request, 'missions.html', {'missions': missions})

def login_view(request):
    return render(request, 'login.html')