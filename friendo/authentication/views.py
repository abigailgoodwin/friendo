# Django Imports
from django.shortcuts import render

# Python3 Imports

# Our Imports
from authentication.forms import RegistrationForm # User registration form.

def register(request):
    '''The view that handles account creation/registration.'''
    form = RegistrationForm()
    return render(request=request, template_name='authentication/register.html', context={'form' : form})
    