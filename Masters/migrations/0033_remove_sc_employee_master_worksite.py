# Generated by Django 4.2.7 on 2024-10-09 13:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Masters', '0032_remove_slotdetails_worksite_slotdetails_site_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sc_employee_master',
            name='worksite',
        ),
    ]