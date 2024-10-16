# Generated by Django 4.2.7 on 2024-10-17 05:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Payroll', '0009_alter_site_card_relation_unique_together_and_more'),
        ('Masters', '0032_remove_slotdetails_worksite_slotdetails_site_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='slotdetails',
            name='designation_id',
            field=models.ForeignKey(blank=True, db_column='designation_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='SlotDetails_designation_id', to='Payroll.designation_master'),
        ),
    ]
