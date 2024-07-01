"""
URL configuration for OpenTraffic project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from KulturMap import settings

from apps.home.views import privacidad

urlpatterns = [
    re_path('', include('pwa.urls')),
    re_path('', include('apps.culture.urls')),  # landing page
    path('admin/', admin.site.urls),
    path('privacidad', privacidad, name='privacidad')
]

admin.site.site_header = 'Ekitaldien administrazioa'
admin.site.site_title = 'Ekitaldien administrazioa'
admin.site.index = 'Ekitaldien administrazioa'


if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
