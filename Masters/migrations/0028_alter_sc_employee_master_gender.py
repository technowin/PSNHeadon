# Generated by Django 4.2.7 on 2024-10-07 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Masters', '0027_alter_slotdetails_slot_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sc_employee_master',
            name='gender',
            field=models.TextField(blank=True, null=True),
        ),
    ]