# Generated by Django 4.2.7 on 2024-12-16 11:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Payroll', '0049_alter_bankdetails_created_by_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='BankDetailAPI',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('api_key', models.TextField(blank=True, null=True)),
                ('secret_key', models.TextField(blank=True, null=True)),
                ('url', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bankAPI_created_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'bank_detailAPi',
            },
        ),
    ]