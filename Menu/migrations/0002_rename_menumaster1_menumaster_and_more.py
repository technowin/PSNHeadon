# Generated by Django 4.2.7 on 2024-12-26 11:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Menu', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='MenuMaster1',
            new_name='MenuMaster',
        ),
        migrations.RenameModel(
            old_name='RoleMenuMaster1',
            new_name='RoleMenuMaster',
        ),
        migrations.RenameModel(
            old_name='UserMenuDetails1',
            new_name='UserMenuDetails',
        ),
        migrations.AlterModelTable(
            name='menumaster',
            table='menu_master',
        ),
        migrations.AlterModelTable(
            name='rolemenumaster',
            table='role_menu_master',
        ),
        migrations.AlterModelTable(
            name='usermenudetails',
            table='user_menu_details',
        ),
    ]