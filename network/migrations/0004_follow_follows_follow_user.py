# Generated by Django 4.1.5 on 2023-12-14 16:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_rename_likes_follow_rename_follows_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='follow',
            name='follows',
            field=models.ManyToManyField(null=True, related_name='follows', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='follow',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
    ]
