from django.template import Library

register = Library()

@register.simple_tag(takes_context=True)
def poster(context, user):
    if context['user'] == user:
        return 'vous'
    else:
        return user.username


@register.filter
def all_reviewed(user):
    return [review.ticket for review in user.reviews.all()]


@register.simple_tag(takes_context=True)
def feedback_menu(context, item_name):
    if context['menu'] == item_name:
        return ' active'
    return ''
