# Generated by Django 4.2.7 on 2024-10-29 07:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Masters', '0054_remove_citymaster_state_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='citymaster',
            name='state_id',
            field=models.ForeignKey(blank=True, db_column='state_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='state_city_id', to='Masters.statemaster'),
        ),
    ]
