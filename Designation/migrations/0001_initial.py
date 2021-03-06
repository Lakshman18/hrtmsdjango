# Generated by Django 4.0.3 on 2022-03-26 11:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Department', '0004_alter_department_modifieddate'),
    ]

    operations = [
        migrations.CreateModel(
            name='Designation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deesignationName', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('isActive', models.BooleanField(default=True)),
                ('createdBy', models.CharField(max_length=255)),
                ('createdDate', models.DateField(auto_now_add=True)),
                ('modifiedBy', models.CharField(max_length=255)),
                ('modifiedDate', models.DateField(auto_now=True)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Department.department')),
            ],
        ),
    ]
