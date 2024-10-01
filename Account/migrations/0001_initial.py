# Generated by Django 4.2.7 on 2024-08-23 09:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssignedCompany',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=255)),
                ('company_id', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('href', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('full_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('encrypted_password', models.CharField(max_length=128)),
                ('phone', models.CharField(max_length=15, unique=True)),
                ('first_time_login', models.IntegerField(default=1)),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now)),
                ('password_text', models.CharField(max_length=128)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='password_storage',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('passwordText', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.ForeignKey(blank=True, db_column='created_by', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_id_repos', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'password_storage',
            },
        ),
        migrations.CreateModel(
            name='FilesTest',
            fields=[
                ('file_id', models.AutoField(primary_key=True, serialize=False)),
                ('rec_id', models.DateField(blank=True, null=True)),
                ('rec_type', models.CharField(max_length=255)),
                ('file_name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='files_created', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='files_updated', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'tbl_fileTest',
            },
        ),
        migrations.CreateModel(
            name='error_log',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('method', models.TextField(blank=True, null=True)),
                ('error', models.TextField(blank=True, null=True)),
                ('error_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='error_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'error_log',
            },
        ),
    ]