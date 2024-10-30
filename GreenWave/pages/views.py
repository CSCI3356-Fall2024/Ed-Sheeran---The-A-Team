from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import profile_form, campaign_form, service_form
from .models import user_profile, campaign, service

# Create your views here.
def home_view(request, *args, **kwargs):
    print(args,kwargs)
    print(request.user)
    if request.user.groups.filter(name='Supervisor').exists():
        group_name = "Supervisor"
    else:
        group_name = "Regular User"

    return render(request, 'home.html', {'group_name': group_name})

def campaign_view(request):
    if request.user.groups.filter(name='Supervisor').exists():
        if request.method == 'POST':
            form = campaign_form(request.POST)
            if form.is_valid():
                form.save()
                return redirect('home')
        else:
             form = campaign_form()
        return render(request, 'campaigns.html', {'form': form})
    else:
         return redirect('/')
    
def service_detail(request, service_id):
    serv = service.objects.get(id = service_id)
    return render(request, 'service_detail.html', {'service': serv})

def service_create(request):
    if request.method == 'POST':
        form = service_form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('service_list') #where do we want to redirect, can I make it unique per service by an ID or new page?
    else:
        form = service_form()
    
    return render(request, 'service_form.html', {'form': form})

def service_list(request):
    serv = service.objects.all()  # Get all service instances
    return render(request, 'service_list.html', {'services': service})

def navbar_view(request):
    if request.user.groups.filter(name='Supervisor').exists():
        group_name = "Supervisor"
    else:
        group_name = "Regular User"
    return render(request, 'navbar.html', {'group_name': group_name})

def profile_view(request):
    user_profile_instance = user_profile.objects.filter(user=request.user).first()

    if request.method == 'POST':
        if 'update' in request.POST:
            form = profile_form(instance=user_profile_instance)
        else:
            form = profile_form(request.POST, request.FILES)
            if form.is_valid():
                if user_profile_instance:
                    profile = form.save(commit=False)
                    profile.user = request.user
                    profile.id = user_profile_instance.id
                    profile.save()
                else:
                    profile = form.save(commit=False)
                    profile.user = request.user
                    profile.save()
                return redirect('home')

    else:
        form = profile_form(instance=user_profile_instance)


    return render(request, "profile.html", {'form':form, 'user_profile': user_profile_instance})

def service_detail_view(request):
	return render(request, "service_detail.html", {})

def service_list_view(request):
	return render(request, "service_list.html", {})

def rewards(request):
	return render(request, "rewards.html", {})