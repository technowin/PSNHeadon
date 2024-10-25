# Generated by Django 4.2.7 on 2024-10-21 05:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Masters', '0045_remove_sc_employee_master_designation_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userslotdetails',
            name='company_id',
            field=models.ForeignKey(blank=True, db_column='company_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='UserSlotDetails_company_id', to='Masters.company_master'),
        ),
    ]
