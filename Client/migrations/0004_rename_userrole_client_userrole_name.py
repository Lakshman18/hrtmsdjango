# Generated by Django 4.0.3 on 2022-04-14 03:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Client', '0003_client_userrole'),
    ]

    operations = [
        migrations.RenameField(
            model_name='client',
            old_name='userRole',
            new_name='userRole_name',
        ),
    ]