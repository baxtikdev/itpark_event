from django.db import models
from users.models import User


class DevicesService(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Place(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class SnacksService(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # responsible_user = models.ForeignKey(ResponsibleUser, related_name='responsible_user', on_delete=models.SET_NULL,
    #                                      null=True, blank=True)
    devices = models.ManyToManyField(DevicesService, blank=True)
    title = models.CharField(max_length=256)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    file = models.FileField(null=True, upload_to="order_files", blank=True)
    date = models.DateField()
    start = models.TimeField()
    end = models.TimeField()
    people_number = models.IntegerField()
    comment = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Quantity(models.Model):
    order = models.ForeignKey(Order, related_name='order_snack_quantity', on_delete=models.CASCADE)
    snack = models.ForeignKey(SnacksService, on_delete=models.CASCADE)
    number = models.IntegerField()

    class Meta:
        verbose_name = "Snack"
        verbose_name_plural = "Number of Snacks"

    def __str__(self):
        return f"{self.number}"
