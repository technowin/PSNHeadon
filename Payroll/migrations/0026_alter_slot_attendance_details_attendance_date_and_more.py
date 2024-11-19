# Generated by Django 4.2.7 on 2024-11-19 05:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Masters', '0059_delete_pooldetails'),
        ('Payroll', '0025_rename_card_id_site_card_relation_card_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slot_attendance_details',
            name='attendance_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='slot_attendance_details',
            name='site_id',
            field=models.ForeignKey(blank=True, db_column='site_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attendance_site_id1', to='Masters.site_master'),
        ),
    ]