# Generated by Django 4.0.3 on 2022-03-06 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Department', '0002_alter_department_createddate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='modifiedBy',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='department',
            name='modifiedDate',
            field=models.DateField(null=True),
        ),
    ]