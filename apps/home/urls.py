from django.urls import path, re_path, include
from .views import home, privacidad
app_name = 'home'

urlpatterns = [
    path('', home, name='home'),
]
