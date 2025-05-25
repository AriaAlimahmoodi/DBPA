from django.shortcuts import render
from .models import Mission, News, Ad  # فرضی مدل‌ها

def home(request):
    # فرضا میخوای اخبار روز خاورمیانه رو تو صفحه اصلی نمایش بدی
    latest_news = News.objects.order_by('-date')[:5]
    return render(request, 'core/home.html', {'news_list': latest_news})

def missions(request):
    missions = Mission.objects.all()
    return render(request, 'core/missions.html', {'missions': missions})

def news(request):
    news_list = News.objects.all()
    return render(request, 'core/news.html', {'news_list': news_list})

def ads(request):
    ads_list = Ad.objects.all()
    return render(request, 'core/ads.html', {'ads_list': ads_list})

def about(request):
    return render(request, 'core/about.html')
