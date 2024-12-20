# Generated by Django 4.2.7 on 2024-10-21 05:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Masters', '0040_remove_sc_employee_master_designation_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee_designation',
            name='company_id',
            field=models.ForeignKey(blank=True, db_column='company_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comapny_designation_relation', to='Masters.company_master'),
        ),
        migrations.AddField(
            model_name='employee_site',
            name='company_id',
            field=models.ForeignKey(blank=True, db_column='company_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comapny_site_relation', to='Masters.company_master'),
        ),
    ]
