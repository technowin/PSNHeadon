# Generated by Django 4.2.7 on 2024-10-09 06:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Masters', '0031_slotdetails_end_time_slotdetails_night_shift_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='slotdetails',
            name='worksite',
        ),
        migrations.AddField(
            model_name='slotdetails',
            name='site_id',
            field=models.ForeignKey(blank=True, db_column='site_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='SlotDetails_site_id', to='Masters.site_master'),
        ),
    ]