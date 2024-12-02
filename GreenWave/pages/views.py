from django.http import HttpResponse
from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404
from .forms import profile_form, campaign_form, service_form, points_form, score_form, reward_form, exchange_points_form
from .models import user_profile, campaign, service, reward, score, transaction
from django.utils import timezone
from django.contrib.auth.models import AnonymousUser
from django.views.generic import ListView

# Create your views here.
def home_view(request, *args, **kwargs):
    print(args,kwargs)
    print(request.user)
    today = timezone.now().date()
    leaderboard = user_profile.objects.order_by('-points')[:10]  # Top 10 users
    campaigns = campaign.objects.filter(start_date__lt=today, end_date__gt=today)
    if request.user.groups.filter(name='Supervisor').exists():
        group_name = "Supervisor"
    else:
        group_name = "Regular User"

    #this does the points if you need it

    #if isinstance(request.user, AnonymousUser):
    #    points = 0
    #else:
    #    points = user_profile.objects.filter(user=request.user).values_list("points", flat=True).first() or 0
    #context = {
    #    'group_name': group_name,
    #    'campaigns': campaigns,
    #    'points' : points,
    #}
    if isinstance(request.user, AnonymousUser):
        points = 0
    else:
        points = user_profile.objects.filter(user=request.user).values_list("points", flat=True).first() or 0
        """fake_campaigns = [
        {
            'name': 'Clean the Beach',
            'start_date': today.strftime('%Y-%m-%d'),
            'end_date': (today + timezone.timedelta(days=7)).strftime('%Y-%m-%d'),
            'points': 100,
            'places': ['Beach A', 'Beach B'],
            'description': 'Join us to clean up the local beach and earn points!',
        },
        {
            'name': 'Plant Trees in Park',
            'start_date': today.strftime('%Y-%m-%d'),
            'end_date': (today + timezone.timedelta(days=14)).strftime('%Y-%m-%d'),
            'points': 150,
            'places': ['Hillside', 'Coro'],
            'description': 'Help plant trees in the city parks to make the environment greener!',
        },
        {
            'name': 'Recycle Plastic Bottles',
            'start_date': today.strftime('%Y-%m-%d'),
            'end_date': (today + timezone.timedelta(days=10)).strftime('%Y-%m-%d'),
            'points': 50,
            'places': ['Community Center', 'Library'],
            'description': 'Collect and recycle plastic bottles in the community. Help reduce waste!',
        }
    ]

    # fake_leaderboard = [
    #     {'rank': 1, 'username': 'Ike', 'points': 500 },
    #     {'rank': 2, 'username': 'Hannah', 'points': 450},
    #     {'rank': 3, 'username': 'Neff', 'points': 300},
    #     {'rank': 4, 'username': 'Matt', 'points': 120},
    #     {'rank': 5, 'username': 'Luke', 'points': 90}
    # ]
"""
    context = {
        'group_name': group_name,
        'campaigns': campaigns,
        'points1': points,
        'leaderboard': [
            {'rank': index + 1, 'username': entry.user.username, 'points': entry.points}
            for index, entry in enumerate(leaderboard)
        ],
        'user': request.user,  # Add user details for personalization
        'points': getattr(request.user.userprofile, 'points', 0) if request.user.is_authenticated else 0,
        # Include other data if necessary
    }

    return render(request, 'home.html', context)

def logout_view(request):
    logout(request)
    return render(request, 'home.html')

def campaign_view(request):
    if request.user.groups.filter(name='Supervisor').exists():
        group_name = "Supervisor"
        if request.method == 'POST':
            form = campaign_form(request.POST)
            if form.is_valid():
                campaign_instance = form.save()
                form._save_m2m()
                return redirect('home')
        else:
             form = campaign_form()
        return render(request, 'campaigns.html', {'form': form, 'group_name': group_name})
    else:
         group_name = "Regular User"
         return redirect('/')

def service_detail(request, service_id):
    serv = service.objects.get(id = service_id)
    return render(request, 'service_detail.html', {'service': serv})

def service_create(request):
    if request.method == 'POST':
        form = service_form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('service_list')
    else:
        form = service_form()

    return render(request, 'service_form.html', {'form': form})

def service_list(request):
    if request.user.groups.filter(name='Supervisor').exists():
        group_name = "Supervisor"
    else:
        group_name = "Regular User"
    serv = service.objects.all()
    return render(request, 'service_list.html', {'services': service, 'group_name': group_name})

def navbar_view(request):
    if request.user.groups.filter(name='Supervisor').exists():
        group_name = "Supervisor"
    else:
        group_name = "Regular User"
    return render(request, 'navbar.html', {'group_name': group_name})

def profile_view(request):
    user_profile_instance = user_profile.objects.filter(user=request.user).first()
    if request.user.groups.filter(name='Supervisor').exists():
        group_name = "Supervisor"
    else:
        group_name = "Regular User"
    if request.method == 'POST':
        if 'update' in request.POST:
            form = profile_form(instance=user_profile_instance)
        else:
            form = profile_form(request.POST, request.FILES, instance=user_profile_instance)
            if form.is_valid():
                if user_profile_instance:
                    profile = form.save(commit=False)
                    profile.user = request.user
                    profile.id = user_profile_instance.id
                    profile.save()
                    return redirect('profile')
                else:
                    profile = form.save(commit=False)
                    profile.user = request.user
                    profile.save()
                    return redirect('home')

    else:
        form = profile_form(instance=user_profile_instance)


    return render(request, "profile.html", {'form':form, 'user_profile': user_profile_instance, 'group_name': group_name})

def service_detail_view(request, id):
    if request.user.groups.filter(name='Supervisor').exists():
        group_name = "Supervisor"
    else:
        group_name = "Regular User"

    service_single = get_object_or_404(service, id=id)
    context = {
        'service': service_single,
        'group_name': group_name,
    }
    return render(request, "service_detail.html", context)

def service_list_view(request):
    if request.user.groups.filter(name='Supervisor').exists():
        group_name = "Supervisor"
    else:
        group_name = "Regular User"

    services = service.objects.all()
    context = {
        'services': services,
        'group_name': group_name,
    }
    return render(request, "service_list.html", context)

def rewards(request):
    if request.user.groups.filter(name='Supervisor').exists():
        group_name = "Supervisor"
        all_rewards = reward.objects.all()

        if request.method == 'POST':
            form = reward_form(request.POST, request.FILES)
            if form.is_valid():
                reward_object = form.save(commit=False)
                reward_object.save()
                reward_object.places.set(form.cleaned_data['places'])
                reward_object.save()
                return redirect('rewards')
        else:
            form = reward_form()
        context = {
            'group_name': group_name,
            'all_rewards': all_rewards,
            'form': form,
        }
    else:
        group_name = "Regular User"
        points = user_profile.objects.filter(user=request.user).values_list("points", flat=True).first() or 0
        transactions = transaction.objects.filter(user_profile__user=request.user).order_by('-date')
        context = {
            'group_name': group_name,
            'next_level_threshold': 1000,
            "points" : points,
            "transactions" : transactions,
        }
    # New, trying to make Bar
    return render(request, "rewards.html", context)

def exchange(request):
    if request.user.groups.filter(name='Supervisor').exists():
        group_name = "Supervisor"
    else:
        group_name = "Regular User"

    points = user_profile.objects.filter(user=request.user).values_list("points", flat=True).first() or 0

    today = timezone.now().date()
    rewards = reward.objects.filter(start_date__lt=today, end_date__gt=today)
    
    context = {
        'group_name': group_name,
        "points" : points,
        'rewards': rewards,
    }
    return render(request, "exchange.html", context)

def exchange_detail_view(request, id):
    if request.user.groups.filter(name='Supervisor').exists():
        group_name = "Supervisor"
    else:
        group_name = "Regular User"

    exchange_single = get_object_or_404(reward, id=id)
    if request.method == 'POST':
        profile = user_profile.objects.get(user=request.user)
        points = profile.points
        if points >= exchange_single.cost:
            profile.points -= exchange_single.cost

            #instance to record the exchange
            trans = transaction(
                user_profile=profile, #I think this works but mine never did without so idk, someone should test sorry
                points=exchange_single.cost,
                place=exchange_single.name,  #havent thought this through yet
                description=f"Exchanged for {exchange_single.name} reward"
            )
            trans.save()

            profile.save()
            return redirect('/rewards')
        #else:
            #This is when the user doesn't have enough points for the exchange

    context = {
        'exchange': exchange_single,
        'group_name': group_name,
    }
    return render(request, "exchange_detail.html", context)

def input(request):
    profile = user_profile.objects.get(user=request.user)

    if request.method == 'POST':
        form = points_form(request.POST)
        if form.is_valid():
            campaign_choice = form.cleaned_data['campaign_choice']

            points = profile.points
            updated_points = points + campaign_choice.points

            profile.points = updated_points

            profile.save()

            return redirect('/')
    else:
        form = points_form()

    points_value = user_profile.objects.filter(user=request.user).values_list("points", flat=True).first() or 0
    return render(request, 'input.html', {'form': form, 'points': points_value})

def add_score(request):
    if request.method == "POST":
        form = score_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('leaderboard')  # Redirect to the leaderboard after submission
    else:
        form = score_form()

    return render(request, 'add_score.html', {'form': form})


"""
def leaderboard_view(request):
    # Fetch all users and order them by points descending
    leaderboard = user_profile.objects.order_by('-points')[:10]  # Top 10 users

    context = {
        'leaderboard': [
            {'rank': index + 1, 'username': entry.user.username, 'points': entry.points}
            for index, entry in enumerate(leaderboard)
        ]
    }
    return render(request, 'leaderboard.html', context)"""

def leaderboard_view(request):
    leaderboard = user_profile.objects.order_by('-points')[:10] 
    profile = user_profile.objects.get(user=request.user)
    
    max_points = leaderboard[0].points if leaderboard else 1 
    percents = (profile.points / max_points) * 100

    context = {
        'leaderboard': [
            {
                'rank': index + 1, 
                'username': entry.user.username, 
                'points': entry.points,
                #'points_percentage': percents
            }
            for index, entry in enumerate(leaderboard)
        ]
    }
    return render(request, 'leaderboard.html', context)