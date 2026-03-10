from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):

    ROLE_CHOICES = (
        ('senior', 'Senior'),
        ('junior', 'Junior')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default="junior"
    )

    bio = models.TextField(blank=True)

    profile_pic = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.user.username