# Django Imports
from django.shortcuts import render, redirect

# Python3 Imports

# Our Imports
from authentication.forms import RegistrationForm, LoginForm # User registration and login forms.

def register(request):
    '''The view that handles account creation/registration.'''
    # User is attempting to create an account.
    form = RegistrationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            # Redirect to log in page.
            return redirect('authentication:login')
    
    return render(request=request, template_name='authentication/register.html', context={'form' : form})
    
def login(request):
    '''The view that handles user logins.'''
    form = LoginForm(request.POST or None)
    return render(request=request, template_name='authentication/login.html', context={'form' : form})