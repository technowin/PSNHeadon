# Generated by Django 4.2.7 on 2025-01-15 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tax', '0010_alter_taxcalculation_act'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taxcalculation',
            name='city',
            field=models.IntegerField(blank=True, max_length=50, null=True),
        ),
    ]
