from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
import uuid


class ImagerProfile(models.Model):
    """A profile for users to our application."""
    user = models.OneToOneField(User)
    location = models.CharField(max_length=100)
    photography_style = models.CharField(max_length=100)
    website = models.CharField(max_length=100)
    joined_date = models.DateField(auto_now=True)


def __repr__(self):
    return self.user.username


@receiver(post_save, sender=User)
def make_profile_new_user(sender, **kwargs):
    if kwargs['created']:
        new_profile = ImagerProfile(
            user=kwargs['instance']
        )
    new_profile.save()
