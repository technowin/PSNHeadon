# Generated by Django 4.2.7 on 2024-10-11 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Payroll', '0005_alter_slot_attendance_details_employee_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slot_attendance_details',
            name='employee_id',
            field=models.TextField(blank=True, max_length=250, null=True),
        ),
    ]
