# Generated by Django 4.2.7 on 2024-09-13 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Masters', '0014_sc_roster_attendance_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sc_roster',
            name='attendance_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
