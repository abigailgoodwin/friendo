# Django Imports
from django.contrib import admin

# Local Imports
from profiles.models import Profile, Hobby, Interest

# Register your models here.
admin.site.register(Profile)
admin.site.register(Hobby)
admin.site.register(Interest)