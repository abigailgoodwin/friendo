# Django Imports
from django.db import models
from django.contrib.auth.models import User

# Python3 Imports
from datetime import date # Used to calculate the user's age.

class Hobby(models.Model):
    '''Defines a Hobby model that represents a hobby. Users can have many of these listed.'''
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=400)
    icon = models.ImageField(default='default/placeholder.png', upload_to='hobby_interest_images')
    
    def __str__(self):
        return self.name
    
class Interest(models.Model):
    '''Defines an Interest model that represents an interest that a user can have.'''
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=200)
    icon = models.ImageField(default='default/placeholder.png', upload_to='hobby_interest_images')
    
    def __str__(self):
        return self.name

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
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    profile_image = models.ImageField(default='default/placeholder.png', upload_to='profile_images')
    location = models.CharField(max_length=200, default='friendo')
    bio = models.TextField(default="Tell us something about yourself!")
    birthday = models.DateField()
    age = models.PositiveSmallIntegerField()
    gender = models.CharField(max_length=50, blank=True)
    seeking_romance = models.BooleanField(default=False)
    hobbies = models.ManyToManyField(Hobby, related_name='profiles', blank=True)
    interests = models.ManyToManyField(Interest, related_name='profiles', blank=True)
    friends = models.ManyToManyField("self", related_name='friends', blank=True)
    first_visit = models.BooleanField(default=True)
    
    def __str__(self):
        return self.user.username
    
    def calculateAge(self):
        '''Calculates the user's current age.'''
        today = date.today()
        age = today.year - self.birthday.year - ((today.month, today.day) < (self.birthday.month, self.birthday.day))
        if age != self.age:
            self.age = age
            self.save()
            