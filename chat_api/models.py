from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model

class DmMessage(models.Model):
    sender = models.ForeignKey(User, related_name="sender_dm_message", on_delete=models.CASCADE)
    reciever = models.ForeignKey(User, related_name="receiver_dm_message", on_delete=models.CASCADE)
    message = models.TextField(null=False)
    create_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.sender)

class Group(models.Model):
    name = models.CharField(max_length=16, null=False)
    owner = models.ForeignKey(User, related_name="owner_group", on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name="users_group")
    create_date = models.DateTimeField(auto_now=True)

class GmMessage(models.Model):
    sender = models.ForeignKey(User, related_name="sender_gm_message", on_delete=models.CASCADE)
    reciever = models.ForeignKey(Group, related_name="receiver_gm_message", on_delete=models.CASCADE)
    message = models.TextField(null=False)
    create_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.sender)