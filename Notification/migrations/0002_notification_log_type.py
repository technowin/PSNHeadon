# Generated by Django 4.2.7 on 2024-09-13 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Notification', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification_log',
            name='type',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
