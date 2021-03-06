# Generated by Django 4.0.3 on 2022-03-26 11:22

import Department.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Employee', '0009_remove_employee_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='address',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='dateOfJoining',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='department',
            field=models.CharField(max_length=255, null=True, verbose_name=Department.models.Department),
        ),
        migrations.AddField(
            model_name='employee',
            name='designation',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='dob',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='manager',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='employee',
            name='maritualStatus',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='nic',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='phoneNumber',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='religion',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='status',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='userRole',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Employee.role'),
        ),
    ]
