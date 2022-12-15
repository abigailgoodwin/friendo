# Django Imports
from django import forms
from profiles.models import Profile

class UpdateProfileImageForm(forms.ModelForm):
    '''This form allows the user to update their profile picture.'''
    profile_image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control',
                                                           'type': 'file',
                                                           'id': 'formFile'}),
                                     label="Upload your new profile picture:",
                                     required=False)
    class Meta:
        model = Profile
        fields = ['profile_image']