from django.db import models
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
