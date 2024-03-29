# Django Imports
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required # Login decorator.

# Python3 Imports
import operator # For itemgetter mapping.

# Local Imports
from profiles.models import Hobby, Interest, Profile
from profiles.forms import UpdateProfileImageForm

@login_required
def my_profile(request):
    '''Displays the currently logged in user's profile.'''
    # Grab the current user's hobbies, interests, and groups.
    context = {}
    my_profile = Profile.objects.get(user=request.user)
    my_hobbies = my_profile.hobbies.all()
    my_interests = my_profile.interests.all()
    context['hobbies'] = my_hobbies
    context['interests'] = my_interests
    return render(request=request, template_name='profiles/my_profile.html', context=context)

@login_required
def profile(request, profileID):
    '''Displays another user's profile.'''
    context = {}
    profile = Profile.objects.get(id=profileID)
    hobbies = profile.hobbies.all()
    interests = profile.interests.all()
    following = True if profile in request.user.profile.following.all() else False
    
    if request.method == 'POST':
        # User is attempting to follow or unfollow this person.
        if following:
            request.user.profile.following.remove(profile)
            following = False
        else:
            request.user.profile.following.add(profile)
            following = True
            
    context['profile'] = profile
    context['following'] = following
    context['hobbies'] = hobbies
    context['interests'] = interests
    return render(request=request, template_name='profiles/profile.html', context=context)

@login_required
def edit_profile(request):
    '''The view that puts the user into edit mode on their profile.'''
    context = {}
    my_profile = Profile.objects.get(user=request.user)
    update_photo_form = UpdateProfileImageForm()
    
    if request.method == 'POST':
        # Check if user is changing their profile picture.
        if 'pictureChange' in request.POST:
            update_photo_form = UpdateProfileImageForm(request.POST, request.FILES, instance=my_profile)
            if update_photo_form.is_valid():
                update_photo_form.save()
                my_profile.save()
            return redirect('profiles:edit')
        else:
            # User is attempting to update their profile.
            new_first_name = request.POST.get('first_name', my_profile.user.first_name)
            new_last_name = request.POST.get('last_name', my_profile.user.last_name)
            new_location = request.POST.get('location', my_profile.location)
            new_bio = request.POST.get('bio', my_profile.bio)
            
            my_profile.user.first_name = new_first_name
            my_profile.user.last_name = new_last_name
            my_profile.user.save()
            my_profile.location = new_location
            my_profile.bio = new_bio
            my_profile.save()
            return redirect('profiles:my_profile')
    
    # If this is the user's first time editing their profile, get rid of their first_visit flag.
    my_profile.first_visit = False
    my_profile.save()
    my_hobbies = my_profile.hobbies.all()
    my_interests = my_profile.interests.all()
    context['hobbies'] = my_hobbies
    context['interests'] = my_interests
    context['form'] = update_photo_form
    return render(request=request, template_name='profiles/edit_profile.html', context=context)
    
@login_required
def select_hobbies(request):
    '''This is the page that will display all selectable hobbies for the purposed of updating one's profile.
    '''
    my_hobbies = request.user.profile.hobbies.all()
    if request.method == 'POST':
        # User is attempting to update their hobbies.
        # Get all of the hobbies they selected.
        post_data = list(request.POST.items())[1:]
        hobby_ids = list(map(operator.itemgetter(0), post_data))
        # Check if they have deselected a hobby they had previously saved.
        for hobby in my_hobbies:
            if hobby.id not in hobby_ids:
                request.user.profile.hobbies.remove(hobby)
        
        # Add the new hobbies
        for id in hobby_ids:
            hobby = Hobby.objects.get(id=id)
            request.user.profile.hobbies.add(hobby)
            
        # Redirect the user back to their profile!
        return redirect('profiles:my_profile')
        
    all_hobbies = Hobby.objects.all()
    return render(request=request, template_name='profiles/edit_hobbies.html', context={'all_hobbies': all_hobbies,
                                                                                   'my_hobbies': my_hobbies})
    
@login_required
def select_interests(request):
    '''This is the page that will display all selectable interests for the purposed of updating one's profile.
    '''
    my_interests = request.user.profile.interests.all()
    if request.method == 'POST':
        # User is attempting to update their interests.
        # Get all of the interests that they selected.
        post_data = list(request.POST.items())[1:]
        interest_ids = list(map(operator.itemgetter(0), post_data))
        # Check if they have deselected a hobby they had previously saved.
        for interest in my_interests:
            if interest.id not in interest_ids:
                request.user.profile.interests.remove(interest)
        
        # Add the new hobbies
        for id in interest_ids:
            interest = Interest.objects.get(id=id)
            request.user.profile.interests.add(interest)
            
        # Redirect the user back to their profile!
        return redirect('profiles:my_profile')
        
    all_interests = Interest.objects.all()
    return render(request=request, template_name='profiles/edit_hobbies.html', context={'all_hobbies': all_interests,
                                                                                   'my_hobbies': my_interests})