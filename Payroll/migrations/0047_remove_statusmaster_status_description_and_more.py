# Generated by Django 4.2.7 on 2024-12-16 10:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Payroll', '0046_rename_company_id_employeeupdate_company'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='statusmaster',
            name='status_description',
        ),
        migrations.DeleteModel(
            name='EmployeeUpdate',
        ),
    ]