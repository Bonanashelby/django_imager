from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.utils.encoding import python_2_unicode_compatible
import uuid


PHOTO_CHOICES = [
    ('BW', 'Black and White'),
    ('PAN', 'Panorama'),
    ('PORT', 'Portrait'),
    ('LAND', 'Landscape'),
    ('FILM', 'Film'),

]

CAMERA_CHOICES = [
    ('CAN', 'Cannon'),
    ('KOD', 'Kodiak'),
    ('NIK', 'Nikon'),
    ('SON', 'Sony'),
    ('IP', 'iPhone')
]


class ImageActiveProfile(models.Manager):
    """Image Active Profile Class Model."""
    def get_queryset(self):
        """Get query set for image active profile."""
        return super(ImageActiveProfile, self).get_queryset().filter(is_active=True)


@python_2_unicode_compatible
class ImagerProfile(models.Model):
    """A profile for users to our application."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    photography_style = models.CharField(
        max_length=5,
        choices=PHOTO_CHOICES,
        default='BW'
    )
    camera_type = models.CharField(
        choices=CAMERA_CHOICES,
        max_length=3,
        default='CAN'
    )
    website = models.CharField(max_length=100)
    joined_date = models.DateField(auto_now=True)
    objects = models.Manager()
    active = ImageActiveProfile()

    @property
    def is_active(self):
        """Active user."""
        return self.user.is_active

    def __repr__(self):
        """Return username."""
        # return self.user.username
        return """
    username: {}
    photography_style: {}
    location: {}
    camera_type: {}
    website: {}
    joined_date: {}
    objects: {}
    active: {}
    """.format(self.user.username, self.photography_style, self.location, self.camera_type, self.website, self.joined_date, self.objects, self.active)


@receiver(post_save, sender=User)
def make_profile_new_user(sender, **kwargs):
    """."""
    if kwargs['created']:
        new_profile = ImagerProfile(
            user=kwargs['instance']
        )
        new_profile.save()
