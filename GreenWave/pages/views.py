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
    if request.method == 'POST':
        form = profile_form(request.POST)
        if form.is_valid():
            image = form.cleaned_data["image"]
            school = form.cleaned_data["school"]
            year = form.cleaned_data["year"]
            major1 = form.cleaned_data["major1"]
            major2 = form.cleaned_data["major2"]
            t = user_profile(school=school, year=year, major1=major1, major2=major2 )
            t.save()
    else:
        form = profile_form()
    return render(request, "profile.html", {'form':form})