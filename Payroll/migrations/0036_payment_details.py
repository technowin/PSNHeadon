# Generated by Django 4.2.7 on 2024-12-06 08:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Payroll', '0035_statusmaster_status_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='payment_details',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('account_number', models.CharField(blank=True, max_length=100, null=True)),
                ('currency', models.TextField(blank=True, max_length=250, null=True)),
                ('mode', models.TextField(blank=True, max_length=250, null=True)),
                ('purpose', models.TextField(blank=True, max_length=250, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_created_by', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
