from django.urls import path
import profiles.views as profile_views

# App Name
app_name = 'profiles'

urlpatterns = [
    path('', profile_views.my_profile, name="my_profile"),
    path('edit/', profile_views.edit_profile, name="edit"),
    path('hobbies/', profile_views.select_hobbies, name="select_hobbies")
]