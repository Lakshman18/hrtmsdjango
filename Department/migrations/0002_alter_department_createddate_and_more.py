# Generated by Django 4.0.3 on 2022-03-06 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Department', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='createdDate',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='department',
            name='modifiedBy',
            field=models.DateField(null=True),
        ),
    ]