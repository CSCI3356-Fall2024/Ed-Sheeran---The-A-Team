from django.http import HttpResponse
from django.shortcuts import render
from .forms import profile_form
from .models import user_profile

# Create your views here.
def home_view(request, *args, **kwargs):
    print(args,kwargs)
    print(request.user)
    return render(request, "home.html", {})

def profile_view(request):
    user_profile_instance = user_profile.objects.filter(user=request.user).first()

    if request.method == 'POST':
        if 'update' in request.POST:
            form = profile_form(instance=user_profile_instance)  # Pre-fill the form for editing
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
                

    else:
        form = profile_form(instance=user_profile_instance)


    return render(request, "profile.html", {'form':form, 'user_profile': user_profile_instance})

def product_detail_view(request):
	return render(request, "product_detail.html", {})

def service_list_view(request):
	return render(request, "service_list.html", {})
