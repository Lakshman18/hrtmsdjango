# Generated by Django 4.0.3 on 2022-03-06 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Employee', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='isActive',
            field=models.CharField(max_length=255),
        ),
    ]
