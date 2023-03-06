import itertools

from django.conf import settings
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from .forms import SignupForm, FollowUserForm, NewTicketForm, TicketAnswerForm
from .models import User, Ticket, Review
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
    context = {
        'page_name': 'Inscritpion',
        'menu': None,
        'form': form,
    }
    return render(request, 'review/signup.html', context=context)


@login_required
def flux(request):
    tickets_lists = [
        request.user.tickets.all(),
        *[follow.tickets.all() for follow in request.user.follows.all()]
    ]
    context = {
        'page_name': 'Flux',
        'menu': 'flux',
        'tickets': sorted(itertools.chain(*tickets_lists), key=lambda ticket: ticket.time_created, reverse=True)
    }
    return render(request, 'review/flux.html', context=context)


@login_required
def posts(request):
    context = {
        'page_name': 'Posts',
        'menu': 'posts',
        'length':[i for i in range(10)]
    }
    return render(request, 'review/posts.html', context=context)


@login_required
def follows(request):
    context = {
        'page_name': 'Abonnements',
        'menu': 'follows',
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
    context = {
        'page_name': 'Nouveau ticket',
        'menu': 'posts'
    }
    if request.method == 'POST':
        ticket_form = NewTicketForm(request.POST, request.FILES)
        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('ticket', ticket.id)
        context['form'] = ticket_form
        return render(request, 'review/new-ticket.html', context=context)
    context['form'] = NewTicketForm()
    return render(request, 'review/new-ticket.html', context=context)


@login_required
def ticket(request, id):
    try:
        curent_ticket = Ticket.objects.get(id=id)
    except Ticket.DoesNotExist:
        raise Http404
    context = {
        'page_name': curent_ticket.title,
        'menu': 'posts',
        'ticket': curent_ticket
    }
    return render(request, 'review/ticket.html', context=context)


@login_required
def ticket_answer(request, id):
    if request.method == 'POST':
        review_form = TicketAnswerForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = Ticket.objects.get(id=id)
            review.save()
            return redirect('review', review.id)
    ticket = Ticket.objects.get(id=id)
    context={
        'page_name': ticket.title,
        'menu': 'posts',
        'ticket':ticket,
        'form': TicketAnswerForm()
    }
    return render(request, 'review/ticket-answer.html', context=context)


@login_required
def review(request, id):
    curent_review = Review.objects.get(id=id)
    context = {
        'page_name': curent_review.headline,
        'menu': 'posts',
        'review': curent_review
    }
    return render(request, 'review/review.html', context=context)
