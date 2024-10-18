# Generated by Django 4.2.7 on 2024-10-17 05:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Masters', '0033_slotdetails_designation_id'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Payroll', '0009_alter_site_card_relation_unique_together_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='daily_salary',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('employee_id', models.TextField(blank=True, max_length=250, null=True)),
                ('attendance_date', models.DateTimeField(blank=True, null=True)),
                ('work_hours', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('element_name', models.TextField(blank=True, null=True)),
                ('pay_type', models.TextField(blank=True, null=True)),
                ('classification', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('created_by', models.ForeignKey(blank=True, db_column='created_by', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='daily_salary_created_by', to=settings.AUTH_USER_MODEL)),
                ('slot_id', models.ForeignKey(db_column='slot_id', on_delete=django.db.models.deletion.CASCADE, related_name='daily_salary_slot_id', to='Masters.slotdetails')),
                ('updated_by', models.ForeignKey(blank=True, db_column='updated_by', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='daily_salary_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'daily_salary',
            },
        ),
    ]