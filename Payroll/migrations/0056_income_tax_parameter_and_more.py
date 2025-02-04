# Generated by Django 5.1.5 on 2025-02-04 09:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Payroll', '0055_incometaxcalculation_incometaxmaster'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='income_tax_parameter',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('tax_parameter', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('created_by', models.ForeignKey(blank=True, db_column='created_by', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='income_tax_parameter_created_by', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, db_column='updated_by', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='income_tax_parameter_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'income_tax_parameter',
            },
        ),
        migrations.AddField(
            model_name='ratecardsalaryelement',
            name='tax_parameter',
            field=models.ForeignKey(blank=True, db_column='tax_parameter', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rate_card_income_related', to='Payroll.income_tax_parameter'),
        ),
        migrations.AddField(
            model_name='salary_element_master',
            name='tax_parameter',
            field=models.ForeignKey(blank=True, db_column='tax_parameter', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='salary_income_related', to='Payroll.income_tax_parameter'),
        ),
    ]
