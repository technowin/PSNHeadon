# Generated by Django 4.2.7 on 2024-10-30 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Notification', '0006_remove_notification_log_slot_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_notification_log',
            name='notification_message',
            field=models.TextField(blank=True, null=True),
        ),
    ]
