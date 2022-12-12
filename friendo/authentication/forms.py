from django import forms # Form classes.
from django.contrib.auth.models import User # User model.
from django.contrib.auth.forms import UserCreationForm # User creation form.
from django.core.exceptions import ValidationError # Used to throw form errors.

class RegistrationForm(UserCreationForm):
    '''The form that users use to register for an account on the site.
    
    Attributes
    ----------
    username_field : CharField
        A field that takes the user's desired username. Must be unique.
    first_name_field : CharField
        A field that takes in the user's first name.
    last_name_field : CharField
        A field that takes in the user's last name.
    email_field : EmailField
        A field that takes in the user's desired email. Must be unique.
    birthday_field : DateField
        A field that stores the user's birthdate. Must be 18 or older to sign up.
    '''
    username_field = forms.CharField(max_length=40, min_length=5, required=True)
    email_field = forms.EmailField()
    first_name_field = forms.CharField(max_length=40, min_length=1, required=True)
    last_name_field = forms.CharField(max_length=40, min_length=1, required=True)
    birthdate_field = forms.DateField(input_formats=['%m-%d-%y', '%m-%d-%Y', '%m/%d/%y', '%m/%d/%Y'], help_text='Enter your birthdate in the MM-DD-YYYY format.', required=True)

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
        
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'birthdate', 'username', 'email', 'password1', 'password2']
