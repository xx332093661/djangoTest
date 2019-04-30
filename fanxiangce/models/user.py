# coding: utf-8

from django.db import models
from django.contrib.auth.models import User
from .photo import Photo
from datetime import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer  # 生成令牌用
from django.conf import settings
from django.utils import timezone
from django.shortcuts import reverse


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=1)

    status = models.CharField(max_length=64, null=1, blank=1)
    liked = models.IntegerField(default=0)
    confirmed = models.BooleanField(default=False)
    like_public = models.BooleanField(default=1)
    name = models.CharField(max_length=64, null=1, blank=1)
    location = models.CharField(max_length=64, null=1, blank=1)
    website = models.CharField(max_length=64, null=1, blank=1)
    background = models.CharField(max_length=64, null=1, blank=1)
    about_me = models.TextField(null=1, blank=1)
    member_since = models.DateTimeField(default=timezone.now)
    last_seen = models.DateTimeField(default=timezone.now)
    avatar_hash = models.CharField(max_length=32, null=1, blank=1)
    followed = models.ManyToManyField(User, blank=True, related_name='followers')

    @property
    def followed_photos(self):
        photo_ids = []
        for f in self.followed.all():
            for photo in f.photos:
                if photo.id not in photo_ids:
                    photo_ids.append(photo.id)
        return Photo.objects.filter(id__in=photo_ids)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(settings.SECRET_KEY, expiration)
        return s.dumps({'confirm': self.user.id})


class MyUser(User):
    class Meta:
        proxy = True


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()