# Django Imports
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required # Login decorator.

# Local Imports
from profiles.models import Profile

@login_required
def home(request):
    '''This view corresponds to the home/landing page, which includes the user's feed.'''
    context = {}
    my_profile = request.user.profile
    followers = Profile.objects.filter(following__id=my_profile.id)
    num_followers = len(followers)
    friend_list = request.user.profile.friends.all()
    num_friends = len(friend_list)
    context['num_followers'] = num_followers
    context['num_friends'] = num_friends
    context['friends'] = friend_list
    context['followers'] = followers
    return render(request=request, template_name='home/home.html', context=context)