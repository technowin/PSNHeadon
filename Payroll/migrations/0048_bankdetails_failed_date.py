# Generated by Django 4.2.7 on 2024-12-16 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Payroll', '0047_remove_statusmaster_status_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bankdetails',
            name='failed_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
