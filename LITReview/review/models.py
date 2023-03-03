from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    follows = models.ManyToManyField(
        'self',
        through='UserFollows',
        related_name='followers',
        through_fields=('user', 'followed_user'),
        symmetrical=False
    )


class UserFollows(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    followed_user = models.ForeignKey(
        User,
        related_name='follower_relation',
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('user', 'followed_user')


class Ticket(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(
        max_length=2048,
        blank=True
    )
    image = models.ImageField(
        null=True,
        blank=True
    )
    time_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='tickets'
    )

    @property
    def time_created_as_text(self):
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
        month = months[self.time_created.month-1]
        return self.time_created.strftime(f'%H:%M:%S le %d {month} %Y')
