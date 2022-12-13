# Django Imports
from django import forms # Form classes.
from django.contrib.auth.models import User # User model.
from django.contrib.auth.forms import UserCreationForm # User creation form.
from django.core.exceptions import ValidationError # Used to throw form errors.

# Python3 Imports
from datetime import date # Used for date comparisons.

# Local Imports
from authentication.models import Profile

class RegistrationForm(UserCreationForm):
    '''The form that users use to register for an account on the site.
    
    Attributes
    ----------
    email_field : EmailField
        A field that takes in the user's desired email. Must be unique. Also used as the user's login credentials.
    username_field : CharField
        A field that takes the user's desired username. Must be unique.
    first_name_field : CharField
        A field that takes in the user's first name.
    last_name_field : CharField
        A field that takes in the user's last name.
    birthday_field : DateField
        A field that stores the user's birthdate. Must be 18 or older to sign up.
    '''
    email = forms.EmailField(required=True)
    username = forms.CharField(max_length=40, min_length=5, required=True)
    first_name = forms.CharField(max_length=40, min_length=1, required=True)
    last_name = forms.CharField(max_length=40, min_length=1, required=True)
    birthdate = forms.DateField(required=True, widget=forms.NumberInput(attrs={'type': 'date', 'id': 'birthdate'}))

    def clean_username_field(self):
        ''' Determines whether or not the username entered is already associated with an account.'''
        new_username = self.cleaned_data['username_field']
        if User.objects.filter(username=new_username).exists():
            raise ValidationError("Sorry, that username is already taken.")
        return new_username
    
    def clean_email_field(self):
        ''' Determines whether or not the e-mail entered is already associated with an account.'''
        new_email = self.cleaned_data['email_field']
        if User.objects.filter(email=new_email).exists():
            raise ValidationError("That e-mail is already tied to an existing account.")
        return new_email
    
    def clean_birthdate_field(self):
        ''' Determines if the user is old enough to be registered for the site.'''
        birthdate = self.cleaned_data['birthdate_field']
        eligible_birth_year = date.today().year - 18
        if birthdate.year > eligible_birth_year:
            raise ValidationError("You must be 18 years or older to register for Friendo.")
        elif birthdate.year == eligible_birth_year:
            if birthdate.month < date.today().month:
                raise ValidationError("You must be 18 years or older to register for Friendo.")
            elif birthdate.month == date.today().month:
                if birthdate.day > date.today().day:
                    raise ValidationError("You must be 18 years or older to register for Friendo.")
    
    def save(self, commit=True):
        '''Attempts to create the user's account and Profile.''' 
        if not commit:
            raise NotImplementedError("Must have database save priveleges to create this user.")
        
        user = super(RegistrationForm, self).save(commit=True)
        user = User.objects.create_user(username=self.cleaned_data['email'], email=self.cleaned_data['email'], password=self.cleaned_data['password1'])
        profile = Profile(user=user, birthday=self.cleaned_data['birthdate_field'])
        profile.save()
        
        return user, profile
    
    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'birthdate']