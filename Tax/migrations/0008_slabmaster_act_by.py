# Generated by Django 4.2.7 on 2025-01-13 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tax', '0007_remove_slabmaster_slab_due_months'),
    ]

    operations = [
        migrations.AddField(
            model_name='slabmaster',
            name='act_by',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
