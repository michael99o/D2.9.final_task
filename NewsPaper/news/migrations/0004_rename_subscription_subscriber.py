# Generated by Django 5.0.1 on 2024-12-18 19:42

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_subscription'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Subscription',
            new_name='Subscriber',
        ),
    ]
