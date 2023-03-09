from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from review.models import Ticket, Review, UserFollows

UserModel = get_user_model()

USERS = [
    {
        'username':'jean8597',
        'password':'motdepasse',
    },
    {
        'username':'sarahj',
        'password':'motdepasse',
    },
    {
        'username':'jean_5679',
        'password':'motdepasse',
    },
]


class Command(BaseCommand):

    help = 'Initialize project for local test'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING(self.help))

        UserModel.objects.all().delete()
        users_list = []
        for user in USERS:
            curent_user = UserModel.objects.create_user(user['username'], f"{user['username']}@litreview.com",user['password'])
            curent_user.save()
            users_list += [curent_user]
            ticket = Ticket.objects.create(
                title='A brief history of time - Stephen Hawking',
                description='Description',
                user=curent_user
            )
            ticket.image.name = 'a-brief-history-of-time-from-stephen-hawking-carl-sagan-first-edition-signed.jpg'
            ticket.save()
        for user in users_list[:2]:
            for ticket in user.tickets.all():
                review = Review.objects.create(
                    headline='Captivant !',
                    body='Description',
                    user=users_list[0],
                    rating=3,
                    ticket=ticket
                )
                review.save()
        follow = UserFollows.objects.create(
            user=users_list[0],
            followed_user=users_list[1]
        )

        self.stdout.write(self.style.SUCCESS("All Done !"))
