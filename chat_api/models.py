from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model

class Dm(models.Model):
    sender = models.ForeignKey(User, related_name="sender_dm", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="receiver_dm", on_delete=models.CASCADE)
    message = models.TextField(null=False)
    create_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.sender)

class Group(models.Model):
    name = models.CharField(max_length=16, null=False, unique=True)
    owner = models.ForeignKey(User, related_name="owner_group", on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name="users_group")
    create_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pk) + " " + self.name

class Gm(models.Model):
    sender = models.ForeignKey(User, related_name="sender_gm", on_delete=models.CASCADE)
    receiver = models.ForeignKey(Group, related_name="receiver_gm", on_delete=models.CASCADE)
    message = models.TextField(null=False)
    create_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.sender)
