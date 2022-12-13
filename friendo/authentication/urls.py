from django.urls import path
import authentication.views as auth_views

# App Name
app_name = 'authentication'

urlpatterns = [
    path('register/', auth_views.register, name="register")
]