# coding: utf-8

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Message(models.Model):
    body = models.TextField(null=1, blank=1)
    timestamp = models.DateTimeField(default=datetime.now)
    disabled = models.BooleanField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages', null=1, blank=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_messages', null=1, blank=1)
