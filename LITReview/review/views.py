from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from .forms import SignupForm, FollowUserForm
from .models import User
# Create your views here.

def signup(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # auto-login user
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, 'review/signup.html', context={'form': form})

@login_required
def flux(request):
    return render(request, 'review/flux.html', context={'length':[i for i in range(10)]})

@login_required
def posts(request):
    print(request.user.id)
    return render(request, 'review/posts.html', context={'length':[i for i in range(10)]})

@login_required
def follows(request):
    context = {
        'form': FollowUserForm(user=request.user),
        'follows': request.user.follows.all(),
        'followers': request.user.followers.all()
    }
    for user in context['followers']:
        print(user)
    return render(request, 'review/abonnements.html', context=context)

@login_required
def follow_user(request):
    if request.method == 'POST':
        follow_user_form = FollowUserForm(request.user, request.POST)
        if follow_user_form.is_valid():
            follow_user_form.save()
    return redirect('abonnements')

@login_required
def unfollow(request, id):
    request.user.follows.remove(User.objects.get(id=id))
    return redirect('abonnements')