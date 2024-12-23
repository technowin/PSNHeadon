# Generated by Django 4.2.7 on 2024-11-15 08:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Masters', '0059_delete_pooldetails'),
        ('Payroll', '0018_rename_classification_salary_element_master_basis'),
    ]

    operations = [
        migrations.AddField(
            model_name='salary_element_master',
            name='pay_type_new',
            field=models.ForeignKey(blank=True, db_column='pay_type_new', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parameter_pay_relation', to='Masters.parameter_master'),
        ),
    ]
