# Generated by Django 4.0.3 on 2022-03-26 02:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Employee', '0008_employee'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='username',
        ),
    ]