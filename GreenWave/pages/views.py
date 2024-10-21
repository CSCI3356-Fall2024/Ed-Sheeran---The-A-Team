from django.http import HttpResponse
from django.shortcuts import render
from .forms import profile_form

# Create your views here.
def home_view(request, *args, **kwargs):
    print(args,kwargs)
    print(request.user)
    return render(request, "home.html", {})

def profile_view(response):
    #if request.method == 'POST':
        #form = profile_form(request.POST)
    return render(response, "profile.html", {})