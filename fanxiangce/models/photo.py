# coding: utf-8

from django.db import models
from django.contrib.auth.models import User
from .album import Album
from datetime import datetime


class Photo(models.Model):
    url = models.CharField(max_length=200, null=True, blank=True)
    url_s = models.CharField(max_length=200, null=True, blank=True)
    url_t = models.CharField(max_length=200, null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(default=datetime.now, null=True, blank=True)
    order = models.IntegerField(null=True, blank=True, default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者', related_name='photos', null=1, blank=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, verbose_name='相册', related_name='photos', null=1, blank=True)
    photo_liked = models.ManyToManyField(User, verbose_name='收藏者', related_name='photo_likes', blank=True)
