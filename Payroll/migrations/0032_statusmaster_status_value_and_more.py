# Generated by Django 4.2.7 on 2024-11-29 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Payroll', '0031_alter_ratecardsalaryelement_four_hour_amount_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='statusmaster',
            name='status_value',
            field=models.TextField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='statusmaster',
            name='status_name',
            field=models.TextField(blank=True, max_length=100, null=True),
        ),
    ]