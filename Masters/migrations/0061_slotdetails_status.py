# Generated by Django 4.2.7 on 2024-12-02 07:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Payroll', '0033_slot_attendance_details_status'),
        ('Masters', '0060_alter_settingmaster_interval'),
    ]

    operations = [
        migrations.AddField(
            model_name='slotdetails',
            name='status',
            field=models.ForeignKey(blank=True, db_column='status_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='slot_status', to='Payroll.statusmaster'),
        ),
    ]
