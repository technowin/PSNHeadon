# Generated by Django 4.2.7 on 2025-01-15 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tax', '0011_alter_taxcalculation_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taxcalculation',
            name='city',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
