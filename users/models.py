import random
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    # TODO: permession
    email = models.EmailField(_('Email address'), unique=True)
    organization_name = models.CharField(max_length=70, verbose_name=_('Organization'))
    position = models.CharField(max_length=70, verbose_name=_('Position'))
    phone = models.CharField(_('phone'), max_length=255)
    is_verified = models.BooleanField(_('is verified'), default=False)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})


class Code(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number = models.CharField(max_length=6, null=True, blank=True)

    def __str__(self):
        return f"{self.number}"

    def save(self, *args, **kwargs):
        number_list = [x for x in range(10)]
        code_items = ''
        for i in range(6):
            num = random.choice(number_list)
            code_items += str(num)
        self.number = code_items
        super().save(*args, **kwargs)


class ChangedPassword(models.Model):
    user = models.ForeignKey(User, related_name='changed_password_users', on_delete=models.CASCADE)
    password = models.CharField(max_length=10)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email
