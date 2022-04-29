from django.shortcuts import render, redirect
from .forms import PostForm,ProfileForm, RelationshipForm
from .models import Post, Comment, Like, Profile, Relationship
from datetime import datetime, date

from django.contrib.auth.decorators import login_required
from django.http import Http404


# Create your views here.

# When a URL request matches the pattern we just defined, 
# Django looks for a function called index() in the views.py file. 

def index(request):
    """The home page for Learning Log."""
    return render(request, 'FeedApp/index.html')



@login_required #decorator = varifies something, once varified, allows use to following function. Restricts access
def profile(request): #access DB and posting things to website
    #only want ppl logged in to have access to it. (hence decorator)
    profile = Profile.objects.filter(user=request.user) #user refers to currently logged in user. user = fields in profile model. user filter b/c get doesn't work w/ exists
    if not profile.exists(): #checks to see if user has profile, if not, creates one
        Profile.objects.create(user=request.user)
    profile = Profile.objects.get(user=request.user)

    if request.method != 'POST':
        form = ProfileForm(instance=profile)
    else: #request method = "POST", trying to save to DB
        form = ProfileForm(instance=profile, data=request.POST) #grab all info from Profile class for that specific user instance
        if form.is_valid():
            form.save()
            return redirect('FeedApp:profile') #keeps them on the profile page

    context = {'form': form}
    return render(request, 'FeedApp/profile.html', context)


