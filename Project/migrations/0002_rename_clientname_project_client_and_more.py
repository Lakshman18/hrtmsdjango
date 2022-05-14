# Generated by Django 4.0.3 on 2022-04-02 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Project', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='clientName',
            new_name='client',
        ),
        migrations.AlterField(
            model_name='project',
            name='renewalDate',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='startDate',
            field=models.DateField(null=True),
        ),
    ]
