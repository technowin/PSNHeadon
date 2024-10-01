# Generated by Django 4.2.7 on 2024-09-16 05:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Masters', '0015_alter_sc_roster_attendance_date'),
        ('Notification', '0002_notification_log_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification_log',
            name='type',
            field=models.ForeignKey(blank=True, db_column='type_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='type_id_parameter', to='Masters.parameter_master'),
        ),
    ]