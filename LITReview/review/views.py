import itertools

from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from .forms import SignupForm, FollowUserForm, NewTicketForm
from .models import User, Ticket
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
    tickets_lists = [
        request.user.tickets.all(),
        *[follow.tickets.all() for follow in request.user.follows.all()]
    ]
    context = {
        'tickets': sorted(itertools.chain(*tickets_lists), key=lambda ticket: ticket.time_created, reverse=True)
    }
    return render(request, 'review/flux.html', context=context)


@login_required
def posts(request):
    return render(request, 'review/posts.html', context={'length':[i for i in range(10)]})


@login_required
def follows(request):
    context = {
        'form': FollowUserForm(user=request.user),
        'follows': request.user.follows.all(),
        'followers': request.user.followers.all()
    }
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


@login_required
def new_ticket(request):
    if request.method == 'POST':
        ticket_form = NewTicketForm(request.POST, request.FILES)
        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('ticket', ticket.id)
        return render(request, 'review/new-ticket.html', context={'form':ticket_form})
    return render(request, 'review/new-ticket.html', context={'form':NewTicketForm()})


@login_required
def ticket(request, id):
    return render(request, 'review/ticket.html', context={'ticket':Ticket.objects.get(id=id)})