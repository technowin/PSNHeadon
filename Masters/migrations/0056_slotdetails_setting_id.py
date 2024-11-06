# Generated by Django 4.2.7 on 2024-11-06 10:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Masters', '0055_citymaster_state_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='slotdetails',
            name='setting_id',
            field=models.ForeignKey(blank=True, db_column='setting_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='SlotDetails_setting_id', to='Masters.settingmaster'),
        ),
    ]
