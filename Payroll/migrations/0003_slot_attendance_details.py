# Generated by Django 4.2.7 on 2024-10-11 07:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Masters', '0032_remove_slotdetails_worksite_slotdetails_site_id'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Payroll', '0002_site_card_relation_designation_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='slot_attendance_details',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('attendance_date', models.DateTimeField(blank=True, null=True)),
                ('attendance_in', models.TextField(blank=True, null=True)),
                ('employee_id', models.TextField(blank=True, null=True)),
                ('attendance_out', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('company_id', models.ForeignKey(blank=True, db_column='company_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attendance_company_id', to='Masters.company_master')),
                ('created_by', models.ForeignKey(blank=True, db_column='created_by', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='slot_attendance_created_by', to=settings.AUTH_USER_MODEL)),
                ('site_id', models.ForeignKey(blank=True, db_column='site_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attendance_site_id', to='Masters.site_master')),
                ('slot_id', models.ForeignKey(blank=True, db_column='slot_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attendance_slot_id', to='Masters.slotdetails')),
                ('updated_by', models.ForeignKey(blank=True, db_column='updated_by', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='slot_attendance_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'slot_attendance_details',
            },
        ),
    ]
