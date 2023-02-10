import random
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

class UserType(models.IntegerChoices):
    USER = 0, _('USER')
    ADMIN = 1, _('ADMIN')
    HELPER = 2, _('HELPER')

class User(AbstractUser):
    # TODO: permession
    email = models.EmailField(_('Email address'), unique=True)
    organization_name = models.CharField(max_length=70, verbose_name=_('Organization'))
    position = models.CharField(max_length=70, verbose_name=_('Position'))
    phone = models.CharField(_('phone'), max_length=255)
    perm = models.IntegerField(default=UserType.USER, choices=UserType.choices)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})
