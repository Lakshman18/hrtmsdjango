# Generated by Django 4.0.3 on 2022-03-06 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Employee', '0004_alter_role_isactive'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='isActive',
            field=models.BooleanField(default=False),
        ),
    ]