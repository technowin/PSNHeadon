# Generated by Django 4.2.7 on 2024-11-29 05:12

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Masters', '0059_delete_pooldetails'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Notification', '0015_slot_notifiaction_log_type'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='slot_notifiaction_log',
            new_name='slot_notification_log',
        ),
    ]
