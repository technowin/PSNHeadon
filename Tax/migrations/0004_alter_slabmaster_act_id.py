# Generated by Django 4.2.7 on 2025-01-08 10:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Tax', '0003_alter_slab_slab_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slabmaster',
            name='act_id',
            field=models.ForeignKey(blank=True, db_column='act_id', null=True, on_delete=django.db.models.deletion.CASCADE, to='Tax.actmaster'),
        ),
    ]
