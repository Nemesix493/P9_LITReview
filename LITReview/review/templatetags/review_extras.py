from django.template import Library

register = Library()

# Filters

@register.filter
def ticket_or_review(instance):
    return type(instance).__name__


@register.filter
def all_reviewed(user):
    return [review.ticket for review in user.reviews.all()]

@register.filter
def is_reviewed(ticket):
    return len(ticket.reviews.all()) < 1


@register.simple_tag(takes_context=True)
def feedback_menu(context, item_name):
    if context['menu'] == item_name:
        return ' active'
    return ''


@register.filter
def filled_star(number):
    return range(number)


@register.filter
def empty_star(number):
    return range(5-number)

# Simple tags

@register.simple_tag(takes_context=True)
def poster(context, user):
    if context['user'] == user:
        return 'vous'
    else:
        return user.username


@register.simple_tag(takes_context=True)
def display_datetime(context, value):
    months = [
        'Janvier',
        'Février',
        'Mars',
        'Avril',
        'May',
        'Juin',
        'Juillet',
        'Aout',
        'Septembre',
        'Octobre',
        'Novembre',
        'Décembre'
    ]
    month = months[value.month-1]
    return value.strftime(f'à %H:%M:%S le %d {month} %Y')
