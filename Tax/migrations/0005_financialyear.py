# Generated by Django 4.2.7 on 2025-01-10 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tax', '0004_alter_slabmaster_act_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='FinancialYear',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('year', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'financial_year',
            },
        ),
    ]
