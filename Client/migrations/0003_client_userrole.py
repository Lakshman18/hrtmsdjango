# Generated by Django 4.0.3 on 2022-04-03 03:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Client', '0002_rename_status_client_password_client_isactive_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='userRole',
            field=models.CharField(default='client', max_length=255),
        ),
    ]
