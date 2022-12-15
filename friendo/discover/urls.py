from django.urls import path
import discover.views as discover_views

# App Name
app_name = 'discover'

urlpatterns = [
    path('', discover_views.discover_home, name="discover_home"),
    path('friends/', discover_views.discover_friends, name="discover_friends"),
]