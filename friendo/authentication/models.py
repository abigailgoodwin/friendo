# Django Imports
from django.db import models
from django.contrib.auth.models import User

# Python3 Imports
from datetime import date # Used to calculate the user's age.

# Local Imports

class Profile(models.Model):
    '''Defines a Profile model that stands in for the User model.
    
    This model is created mainly to "extend" the existing User model and add
    fields such as hobbies and birthdate.
    
    Attributes
    ----------
    user : OneToOneField
        A one-to-one connection with the Django user created for this profile.
    handle : CharField
        The user's "username", also known as handle, which other users can search for to find this user.
    birthday : datetime
        The user's birthdate.
    age : PositiveSmallIntegerField
        The user's current age; for now, calculated each time their profile is visited.
        
    Methods
    -------
    calculateAge : void
        Calculates the user's current age.
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    handle = models.CharField(max_length=40, default="anonymous")
    birthday = models.DateField()
    age = models.PositiveSmallIntegerField()
    
    def __str__(self):
        return self.handle
    
    def calculateAge(self):
        '''Calculates the user's current age.'''
        today = date.today()
        age = today.year - self.birthday.year - ((today.month, today.day) < (self.birthday.month, self.birthday.day))
        if age != self.age:
            self.age = age
            self.save()