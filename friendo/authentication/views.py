# Django Imports
from django.shortcuts import render, redirect # Used for page redirecting.
from django.contrib import auth # Used for login.
from django.contrib.auth.models import User # Used for logging the user in.
from django.contrib.auth.decorators import login_required # Login decorator.

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
    form = LoginForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            
            if user is not None:
                auth.login(request, user)
                user = User.objects.get(username=username)
                if user is not None:
                    return redirect('home:home')
    
    return render(request=request, template_name='authentication/login.html', context={'form' : form})

@login_required
def logout(request):
    '''The view that handles user logout requests.'''
    auth.logout(request)
    return redirect('authentication:login')