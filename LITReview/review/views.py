from django.shortcuts import render

# Create your views here.

def signup(request):
    return render(request, 'review/signup.html')

def signin(request):
    return render(request, 'review/signin.html')

def flux(request):
    return render(request, 'review/flux.html', context={'length':[i for i in range(10)]})

def posts(request):
    return render(request, 'review/flux.html')

def follows(request):
    return render(request, 'review/abonnements.html', context={'length':[i for i in range(10)]})