# Generated by Django 4.2.7 on 2024-11-29 05:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Masters', '0059_delete_pooldetails'),
        ('Notification', '0014_slot_notifiaction_log'),
    ]

    operations = [
        migrations.AddField(
            model_name='slot_notifiaction_log',
            name='type',
            field=models.ForeignKey(blank=True, db_column='type_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='slot_type_id', to='Masters.parameter_master'),
        ),
    ]
