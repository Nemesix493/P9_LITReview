import itertools

from django.conf import settings
from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from .forms import SignupForm, FollowUserForm, TicketForm, ReviewForm
from .models import User, Ticket, Review
# Create your views here.

def signup(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
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
    posts_list = [
        request.user.tickets.all(),
        *[follow.tickets.all() for follow in request.user.follows.all()],
        request.user.reviews.all(),
        *[follow.reviews.all() for follow in request.user.follows.all()]
    ]
    context = {
        'page_name': 'Flux',
        'menu': 'flux',
        'posts': sorted(itertools.chain(*posts_list), key=lambda ticket: ticket.time_created, reverse=True)
    }
    return render(request, 'review/flux.html', context=context)


@login_required
def posts(request):
    context = {
        'page_name': 'Vos posts',
        'menu': 'posts',
        'posts':sorted(itertools.chain(request.user.reviews.all(), request.user.tickets.all()), key=lambda instance: instance.time_created, reverse=True)
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
    try:
        request.user.follows.remove(User.objects.get(id=id))
    except User.DoesNotExist:
        raise Http404("Il semble que cet utilisateur n'existe pas !")
    return redirect('abonnements')


@login_required
def new_ticket(request):
    context = {
        'page_name': 'Nouveau ticket',
        'menu': 'posts'
    }
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES)
        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('ticket', ticket.id)
        context['form'] = ticket_form
        return render(request, 'review/new-ticket.html', context=context)
    context['form'] = TicketForm()
    return render(request, 'review/new-ticket.html', context=context)


@login_required
def ticket(request, id):
    try:
        curent_ticket = Ticket.objects.get(id=id)
    except Ticket.DoesNotExist:
        raise Http404("Il semble que ce ticket n'existe pas !")
    context = {
        'page_name': curent_ticket.title,
        'menu': 'posts',
        'ticket': curent_ticket
    }
    return render(request, 'review/ticket.html', context=context)


@login_required
def ticket_answer(request, id):
    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = Ticket.objects.get(id=id)
            review.save()
            return redirect('review', review.id)
    try:
        curent_ticket = Ticket.objects.get(id=id)
    except Ticket.DoesNotExist:
        raise Http404("Il semble que ce ticket n'existe pas !")
    context={
        'page_name': curent_ticket.title,
        'menu': 'posts',
        'ticket':curent_ticket,
        'form': ReviewForm()
    }
    return render(request, 'review/ticket-answer.html', context=context)


@login_required
def review(request, id):
    try:
        curent_review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        raise Http404("Il semble que cette critique n'existe pas !")
    context = {
        'page_name': curent_review.headline,
        'menu': 'posts',
        'review': curent_review
    }
    return render(request, 'review/review.html', context=context)


@login_required
def modify_ticket(request, id):
    try:
        curent_ticket = Ticket.objects.get(id=id)
    except Ticket.DoesNotExist:
        raise Http404("Il semble que ce ticket n'existe pas !")
    if curent_ticket.user != request.user:
        raise PermissionDenied('Il semble que vous ne puissiez pas modifier ce ticket car vous n\'en n\'êtes pas l\'auteur')
    context = {
        'page_name': 'Modifier un ticket',
        'menu': 'posts',
    }
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES, instance=curent_ticket)
        if ticket_form.is_valid():
            ticket = ticket_form.save()
            return redirect('ticket', ticket.id)
        context['form'] = ticket_form
        return render(request, 'review/modify_ticket.html', context=context)
    context['form'] = TicketForm(instance=curent_ticket)
    return render(request, 'review/modify_ticket.html', context=context)


@login_required
def modify_review(request, id):
    try:
        curent_review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        raise Http404("Il semble que cette critique n'existe pas !")
    if curent_review.user != request.user:
        raise PermissionDenied('Il semble que vous ne puissiez pas modifier cette critique car vous n\'en n\'êtes pas l\'auteur')
    context = {
        'page_name': 'Modifier une critique',
        'menu': 'posts',
    }
    if request.method == 'POST':
        review_form = ReviewForm(request.POST, instance=curent_review)
        if review_form.is_valid():
            review = review_form.save()
            return redirect('review', review.id)
        context['form'] = review_form
        return render(request, 'review/modify_review.html', context=context)
    context['form'] = ReviewForm(instance=curent_review)
    return render(request, 'review/modify_review.html', context=context)


@login_required
def new_review(request):
    context = {
        'page_name': 'Nouvelle critique',
        'menu': 'posts',
    }
    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        ticket_form = TicketForm(request.POST, request.FILES)
        if review_form.is_valid() and ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            ticket.save()
            review.save()
            return redirect('review', review.id)
        context['review_form'] = review_form
        context['ticket_form'] = ticket_form
        return render(request, 'review/new_review.html', context=context)
    context['review_form'] = ReviewForm()
    context['ticket_form'] = TicketForm()
    return render(request, 'review/new_review.html', context=context)


def custom_404(request, exception):
    context = {
        'page_name': '404 Not found',
        'menu': None,
        'exception': exception
    }
    return render(request, 'review/custom_404.html', context=context)
