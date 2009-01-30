"""
Module responsible for defining models, and implementing
basic object-relations. Implements user profile
"""


from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """
    User profile model, cintains a Foreign Key, which links it to the
    user profile.
    """
    about = models.TextField()
    user = models.ForeignKey(User, unique=True)
