# Generated by Django 4.2.7 on 2025-01-10 09:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Masters', '0064_alter_citymaster_created_by_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='citymaster',
            old_name='state_id',
            new_name='state',
        ),
    ]
