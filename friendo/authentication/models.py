# Django Imports
from django.db import models
from django.contrib.auth.models import User

# Python3 Imports

# Local Imports

class Profile(models.Model):
    '''Defines a Profile model that stands in for the User model.
    
    This model is created mainly to "extend" the existing User model and add
    fields such as hobbies and birthdate.
    
    Attributes
    ----------
    user : OneToOneField
        A one-to-one connection with the Django user created for this profile.
    birthday : datetime
        The user's birthdate.
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField()
    age = models.PositiveSmallIntegerField()