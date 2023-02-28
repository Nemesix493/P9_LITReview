from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.

def signup(request):
    return render(request, 'review/signup.html')

@login_required
def flux(request):
    return render(request, 'review/flux.html', context={'length':[i for i in range(10)]})
@login_required
def posts(request):
    return render(request, 'review/posts.html', context={'length':[i for i in range(10)]})

@login_required
def follows(request):
    return render(request, 'review/abonnements.html', context={'length':[i for i in range(10)]})