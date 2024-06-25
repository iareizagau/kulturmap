from django.urls import path, re_path, include
from .views import culture, event
from .views import HomeView

app_name = 'culture'

urlpatterns = [
    path('', culture, name='home'),
    path('event/<pk>', event, name='event'),
    path("test", HomeView.as_view(), name="test"),

]
