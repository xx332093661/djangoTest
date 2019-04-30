# coding: utf-8

from django.db import models
from datetime import datetime


class Album(models.Model):
    title = models.CharField('标题', max_length=64, null=True, blank=True)
    about = models.TextField(null=1, blank=1)
    cover = models.CharField(max_length=64, null=1, blank=1)
    type = models.IntegerField(default=0)
    tag = models.CharField(max_length=64, null=1, blank=1)
    no_public = models.BooleanField(default=True)
    no_comment = models.BooleanField(default=1)
    asc_order = models.BooleanField(default=1)
    timestamp = models.DateTimeField(default=datetime.now)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='albums', null=True, blank=True)
    album_liked = models.ManyToManyField('auth.User', related_name='album_likes', blank=1)

    def __str__(self):
        return self.title