# Generated by Django 4.2.7 on 2024-11-06 12:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Masters', '0056_slotdetails_setting_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='userslotdetails',
            name='emp_id',
            field=models.ForeignKey(blank=True, db_column='emp_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='UserSlotDetails_emp_id', to='Masters.sc_employee_master'),
        ),
    ]
