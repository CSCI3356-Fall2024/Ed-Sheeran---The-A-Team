from django.http import HttpResponse
from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404
from .forms import profile_form, campaign_form, service_form, points_form
from .models import user_profile, campaign, service, reward
from django.utils import timezone
from django.contrib.auth.models import AnonymousUser

# Create your views here.
def home_view(request, *args, **kwargs):
    print(args,kwargs)
    print(request.user)
    today = timezone.now().date()
    campaigns = campaign.objects.filter(start_date__lt=today, end_date__gt=today)
    if request.user.groups.filter(name='Supervisor').exists():
        group_name = "Supervisor"
    else:
        group_name = "Regular User"

    #this does the points if you need it
    if isinstance(request.user, AnonymousUser):
        points = 0
    else:
        points = user_profile.objects.filter(user=request.user).values_list("points", flat=True).first() or 0
    context = {
        'group_name': group_name,
        'campaigns': campaigns,
        'points' : points,
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
    else:
        group_name = "Regular User"
    # New, trying to make Bar
    points = user_profile.objects.filter(user=request.user).values_list("points", flat=True).first() or 0
    context = {
        'group_name': group_name,
        'current_points': 75, #this is just points so we could remove
        'next_level_threshold': 1000,
        "points" : points
    }
    return render(request, "rewards.html", context)

def exchange(request):
    if request.user.groups.filter(name='Supervisor').exists():
        group_name = "Supervisor"
    else:
        group_name = "Regular User"

    points = user_profile.objects.filter(user=request.user).values_list("points", flat=True).first() or 0
    rewards = reward.objects.all()
    context = {
        'group_name': group_name,
        "points" : points,
        'rewards': rewards,
    }
    return render(request, "exchange.html", context)

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
