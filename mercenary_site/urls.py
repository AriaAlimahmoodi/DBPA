from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),                      # فقط یکبار مسیر admin
    path('', include('core.urls')),      
    path('api/core/', include('core.urls')),                 # مسیرهای اپ core
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

path('', include('core.urls')),
