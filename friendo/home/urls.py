from django.urls import path
import home.views as home_views

# App Name
app_name = 'home'

urlpatterns = [
    path('', home_views.home, name="home")
]