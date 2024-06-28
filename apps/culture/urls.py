from django.urls import path, re_path, include
from .views import culture, event
from .views import HomeView, play_console

app_name = 'culture'

urlpatterns = [
    path('', culture, name='home'),
    path('event/<pk>', event, name='event'),
    path("test", HomeView.as_view(), name="test"),
    path('.well-known/assetlinks.json', play_console, name='play_console'),
]
