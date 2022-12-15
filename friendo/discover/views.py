# Django Imports
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required # Login decorator.

@login_required
def discover_home(request):
    '''The landing page of the Discover part of friendo.'''
    return render(request=request, template_name='discover/discover_home.html')

def discover_friends(request):
    '''This is the starting page of the Discover Friends feature.'''
    return render(request=request, template_name='discover/discover_friends.html')