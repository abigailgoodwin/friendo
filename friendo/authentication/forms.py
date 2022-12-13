# Django Imports
from django import forms # Form classes.
from django.contrib.auth.models import User # User model.
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm # User creation form.
from django.core.exceptions import ValidationError # Used to throw form errors.

# Python3 Imports
from datetime import date # Used for date comparisons.

# Local Imports
from my_profile.models import Profile

class LoginForm(AuthenticationForm):
    '''The form that users use to log in to the site.'''
    
    def __init__(self, *args, **kwargs):
        '''Adds Bootstrap styling to the built-in login fields.'''
        super().__init__(*args,**kwargs)
        for field in self.fields.values() :
            field.widget.attrs["class"] = "form-control"
        self.fields['username'].widget.attrs.update({'id': 'username'})
        self.fields['password'].widget.attrs.update({'id': 'password'})

    class Meta:
        model = User 
        fields = ['username', 'password']

class RegistrationForm(UserCreationForm):
    '''The form that users use to register for an account on the site.
    
    Attributes
    ----------
    email : EmailField
        A field that takes in the user's desired email. Must be unique. Also used as the user's login credentials.
    username : CharField
        A field that takes the user's desired username. Must be unique.
    first_name : CharField
        A field that takes in the user's first name.
    last_name : CharField
        A field that takes in the user's last name.
    birthdate : DateField
        A field that stores the user's birthdate. Must be 18 or older to sign up.
    '''
    email = forms.EmailField(required=True,
                             label="E-Mail",
                             help_text="You will log into Friendo using your e-mail.",
                             widget=forms.EmailInput(attrs={'type': 'email',
                                                            'id': 'email',
                                                            'placeholder': 'email@email.com',
                                                            'aria-describedby': 'emailHelp'}))
    username = forms.CharField(max_length=40,
                               min_length=2,
                               required=True,
                               label="Username",
                               help_text="Your username must be at least 2 characters long.",
                               widget=forms.TextInput(attrs={'id': 'username',
                                                             'placeholder': 'Username',
                                                             'aria-describedby': 'usernameHelp'}))
    first_name = forms.CharField(max_length=40,
                                 min_length=1,
                                 required=True,
                                 label="First Name",
                                 widget=forms.TextInput(attrs={'id': 'first_name',
                                                               'placeholder': 'Waldo'}))
    last_name = forms.CharField(max_length=40,
                                min_length=1,
                                required=True,
                                label="Last Name",
                                widget=forms.TextInput(attrs={'id': 'last_name', 'placeholder': 'Wildcat'}))
    birthdate = forms.DateField(required=True,
                                label="Birth Date",
                                widget=forms.NumberInput(attrs={'type': 'date', 'id': 'birthdate'}))
    
    def __init__(self, *args, **kwargs):
        '''Adds Django widgets to the hidden password1 and password2 fields, and a form-control class to everything.'''
        super().__init__(*args,**kwargs)
        for field in self.fields.values() :
            field.widget.attrs["class"] = "form-control"
        
        self.fields['password1'].label = "Create Password"
        self.fields['password2'].label = "Confirm Password"
        self.fields['password1'].widget.attrs.update({'id': 'password1', 'placeholder':'Password'})
        self.fields['password2'].widget.attrs.update({'id': 'password2', 'placeholder':'Password'})
    
    def clean_username(self):
        ''' Determines whether or not the username entered is already associated with an account.'''
        new_username = self.cleaned_data['username']
        if User.objects.filter(username=new_username).exists():
            raise ValidationError("Sorry, that username is already taken.")
        return new_username
    
    def clean_email(self):
        ''' Determines whether or not the e-mail entered is already associated with an account.'''
        new_email = self.cleaned_data['email']
        if User.objects.filter(email=new_email).exists():
            raise ValidationError("That e-mail is already tied to an existing account.")
        return new_email
    
    def clean_birthdate(self):
        ''' Determines if the user is old enough to be registered for the site.'''
        birthdate = self.cleaned_data['birthdate']
        eligible_birth_year = date.today().year - 18
        if birthdate.year > eligible_birth_year:
            raise ValidationError("You must be 18 years or older to register for Friendo.")
        elif birthdate.year == eligible_birth_year:
            if birthdate.month < date.today().month:
                raise ValidationError("You must be 18 years or older to register for Friendo.")
            elif birthdate.month == date.today().month:
                if birthdate.day > date.today().day:
                    raise ValidationError("You must be 18 years or older to register for Friendo.")
        return birthdate
    
    def save(self, commit=True):
        '''Attempts to create the user's account and Profile.''' 
        if not commit:
            raise NotImplementedError("Must have database save priveleges to create this user.")
        
        user = User.objects.create_user(username=self.cleaned_data['username'],
                                        email=self.cleaned_data['email'],
                                        password=self.cleaned_data['password1'],
                                        first_name=self.cleaned_data['first_name'],
                                        last_name=self.cleaned_data['last_name'])
        # Quickly calculate age to pass to Profile.
        today = date.today()
        age = today.year - self.cleaned_data['birthdate'].year - ((today.month, today.day) < (self.cleaned_data['birthdate'].month, self.cleaned_data['birthdate'].day))
        profile = Profile(user=user, birthday=self.cleaned_data['birthdate'], age=age)
        profile.save()

        return user, profile
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'birthdate']