# Django Imports
from django.contrib import admin
from django.urls import path, include # Used for importing from other URL files.
from django.conf.urls.static import static # Media Options
from django.conf import settings # Media Option

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path('', include('home.urls')),
    path('profile/', include('profiles.urls'))
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
