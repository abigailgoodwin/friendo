# Django Imports
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required # Login decorator.

@login_required
def home(request):
    '''This view corresponds to the home/landing page, which includes the user's feed.'''
    return render(request=request, template_name='home/home.html')