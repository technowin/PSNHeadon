# Generated by Django 4.2.7 on 2024-10-21 06:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Payroll', '0012_remove_income_tax_deduction_deduction_date_and_more'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='income_tax_deduction',
            table='income_tax_deduction',
        ),
        migrations.AlterModelTable(
            name='salary_generated_log',
            table='salary_generated_log',
        ),
    ]
