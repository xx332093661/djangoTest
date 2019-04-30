# Generated by Django 2.1 on 2018-08-29 08:43

import django.contrib.auth.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
        ('fanxiangce', '0004_myuser'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MyUser',
        ),
        migrations.CreateModel(
            name='User',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
