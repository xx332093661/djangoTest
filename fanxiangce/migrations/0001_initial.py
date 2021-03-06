# Generated by Django 2.1 on 2018-08-27 07:39

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=64, null=True, verbose_name='标题')),
                ('about', models.TextField(blank=1, null=1)),
                ('cover', models.CharField(blank=1, max_length=64, null=1)),
                ('type', models.IntegerField(default=0)),
                ('tag', models.CharField(blank=1, max_length=64, null=1)),
                ('no_public', models.BooleanField(default=True)),
                ('no_comment', models.BooleanField(default=1)),
                ('asc_order', models.BooleanField(default=1)),
                ('timestamp', models.DateTimeField(default=datetime.datetime.now)),
                ('album_liked', models.ManyToManyField(blank=1, related_name='album_likes', to=settings.AUTH_USER_MODEL)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='albums', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(blank=1, null=1)),
                ('timestamp', models.DateTimeField(default=datetime.datetime.now)),
                ('disabled', models.BooleanField()),
                ('author', models.ForeignKey(blank=1, null=1, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(blank=1, null=1)),
                ('timestamp', models.DateTimeField(default=datetime.datetime.now)),
                ('disabled', models.BooleanField()),
                ('author', models.ForeignKey(blank=1, null=1, on_delete=django.db.models.deletion.CASCADE, related_name='messages', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=1, null=1, on_delete=django.db.models.deletion.CASCADE, related_name='user_messages', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(blank=True, max_length=200, null=True)),
                ('url_s', models.CharField(blank=True, max_length=200, null=True)),
                ('url_t', models.CharField(blank=True, max_length=200, null=True)),
                ('about', models.TextField(blank=True, null=True)),
                ('timestamp', models.DateTimeField(blank=True, default=datetime.datetime.now, null=True)),
                ('order', models.IntegerField(blank=True, default=0, null=True)),
                ('album', models.ForeignKey(blank=True, null=1, on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='fanxiangce.Album', verbose_name='相册')),
                ('author', models.ForeignKey(blank=True, null=1, on_delete=django.db.models.deletion.CASCADE, related_name='photos', to=settings.AUTH_USER_MODEL, verbose_name='作者')),
                ('photo_liked', models.ManyToManyField(blank=True, related_name='photo_likes', to=settings.AUTH_USER_MODEL, verbose_name='收藏者')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=1, max_length=64, null=1)),
                ('liked', models.IntegerField(default=0)),
                ('confirmed', models.BooleanField(default=False)),
                ('like_public', models.BooleanField(default=1)),
                ('name', models.CharField(blank=1, max_length=64, null=1)),
                ('location', models.CharField(blank=1, max_length=64, null=1)),
                ('website', models.CharField(blank=1, max_length=64, null=1)),
                ('background', models.CharField(blank=1, max_length=64, null=1)),
                ('about_me', models.TextField(blank=1, null=1)),
                ('member_since', models.DateTimeField(default=datetime.datetime.now)),
                ('last_seen', models.DateTimeField(default=datetime.datetime.now)),
                ('avatar_hash', models.CharField(blank=1, max_length=32, null=1)),
                ('followed', models.ManyToManyField(blank=True, related_name='followers', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(null=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='photo',
            field=models.ForeignKey(blank=1, null=1, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='fanxiangce.Photo'),
        ),
    ]
