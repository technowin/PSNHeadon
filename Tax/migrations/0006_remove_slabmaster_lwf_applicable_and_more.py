# Generated by Django 4.2.7 on 2025-01-10 11:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Tax', '0005_financialyear'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='slabmaster',
            name='LWF_Applicable',
        ),
        migrations.RemoveField(
            model_name='slabmaster',
            name='challan_for',
        ),
        migrations.RemoveField(
            model_name='slabmaster',
            name='mode_Of_challan_generation',
        ),
        migrations.RemoveField(
            model_name='slabmaster',
            name='online_url',
        ),
        migrations.RemoveField(
            model_name='slabmaster',
            name='slab_dd',
        ),
        migrations.RemoveField(
            model_name='slabmaster',
            name='slab_due',
        ),
        migrations.RemoveField(
            model_name='slabmaster',
            name='slab_due_months_returns',
        ),
        migrations.RemoveField(
            model_name='slabmaster',
            name='slab_due_returns',
        ),
        migrations.RemoveField(
            model_name='slabmaster',
            name='slab_freq_returns',
        ),
        migrations.RemoveField(
            model_name='slabmaster',
            name='slab_from',
        ),
        migrations.RemoveField(
            model_name='slabmaster',
            name='slab_interest',
        ),
        migrations.RemoveField(
            model_name='slabmaster',
            name='slab_months_challan',
        ),
        migrations.RemoveField(
            model_name='slabmaster',
            name='slab_months_for_returns',
        ),
        migrations.RemoveField(
            model_name='slabmaster',
            name='slab_months_returns',
        ),
        migrations.RemoveField(
            model_name='slabmaster',
            name='slab_note',
        ),
        migrations.RemoveField(
            model_name='slabmaster',
            name='slab_penalty',
        ),
    ]
