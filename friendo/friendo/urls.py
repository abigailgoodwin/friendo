# Django Imports
from django.contrib import admin
from django.urls import path, include # Used for importing from other URL files.

# Python3 Imports

# Local Imports

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path('', include('home.urls'))
]
