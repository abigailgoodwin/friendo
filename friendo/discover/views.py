# Django Imports
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required # Login decorator.
from django.db.models import Q # Used for filtering down objects.

# Local Imports
from profiles.models import Profile

# Python3 Imports
from operator import itemgetter # Used for more efficient sorting.

@login_required
def discover_home(request):
    '''The landing page of the Discover part of friendo.'''
    return render(request=request, template_name='discover/discover_home.html')

def discover_friends(request):
    '''This is the starting page of the Discover Friends feature.'''
    context = {}
    if request.method == 'POST':
        # Get fields from POST request here. Some minor processing to convert strings to bools done here.
        options = {}
        options['filter_romance'] = True if request.POST.get('seeking_romance', 'off') == 'on' else False
        preferred_gender = request.POST.get('gender', None)
        options['preferred_gender'] = None if preferred_gender == 'None' else preferred_gender
        min_age = request.POST.get('min_age', None)
        options['min_age'] = None if min_age == '' else min_age
        max_age = request.POST.get('max_age', None)
        options['max_age'] = None if max_age == '' else max_age
        options['location_on'] = True if request.POST.get('location_on', None) == 'on' else False
        context['filter'] = options
        context['results'] = filterFriends(options=options, requestProfile=request.user.profile)
        context['results'] = rankFriendsByMatchScore(context['results'], requestProfile=request.user.profile)
        
    return render(request=request, template_name='discover/discover_friends.html', context=context)

def filterFriends(options, requestProfile):
    '''This function performs the user filtering for the Discover Friends feature.
    '''
    friend_pool = Profile.objects.all()
    # This line ensures that the user is not included in their search results.
    friend_pool = friend_pool.filter(~Q(id=requestProfile.id))
    
    # Filtering based on the options given.
    if options['filter_romance'] is True:
        friend_pool = friend_pool.filter(seeking_romance=False)
    if options['preferred_gender'] is not None:
        friend_pool = friend_pool.filter(gender=options['preferred_gender'])
        
    if options['min_age'] is not None:
        friend_pool = friend_pool.filter(age__gte=options['min_age'])
        
    if options['max_age'] is not None:
        friend_pool = friend_pool.filter(age__lte=options['max_age'])
        
    if options['location_on']:
        friend_pool = friend_pool.filter(location__icontains=requestProfile.location)
        
    return friend_pool

def rankFriendsByMatchScore(results, requestProfile):
    '''This function ranks the user's friend search results by their match score and sorts them in descending order.
    
    Match score is calculate based on how many hobbies and interests the two users share.
    '''
    # The match score is essentially the number of connection points the two contacts share divided by the total number of
    # possible connections between the two (hobbies + interests).
    ranked_results = []
    my_hobbies = requestProfile.hobbies.all()
    my_interests = requestProfile.interests.all()
    # Calculate how many connection points are available for me.
    my_available_points = len(my_hobbies) + len(my_interests)

    if my_available_points != 0:
        for candidate in results:
            # Collect the hobbies and interests of the candidate.
            their_hobbies = candidate.hobbies.all()
            their_interests = candidate.interests.all()
            
            connectionPoints = 0
            availablePoints = my_available_points
            for hobby in their_hobbies:
                if hobby in my_hobbies:
                    connectionPoints += 1
                else:
                    availablePoints += 1
                    
            for interest in their_interests:
                if interest in my_interests:
                    connectionPoints += 1
                else:
                    availablePoints += 1
            
            # Do final calculation + rounding.
            score = 0
            if connectionPoints != 0:
                score = round((connectionPoints / availablePoints) * 100.0)

            ranked_results.append((candidate, score))
            
        ranked_results = sorted(ranked_results, key=itemgetter(1), reverse=True)
    else:
        for candidate in results:
            ranked_results.append((candidate, 0))
            
    return ranked_results
        
    # Lastly, rank candidates by match score, descending.
    
    