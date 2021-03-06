# Generated by Django 4.0.3 on 2022-04-24 02:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Designation', '0003_rename_deesignationname_designation_designationname'),
        ('Department', '0004_alter_department_modifieddate'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vacancy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no_of_vacancy', models.IntegerField()),
                ('closingDate', models.DateField(null=True)),
                ('createdBy', models.CharField(max_length=255)),
                ('createdDate', models.DateField(auto_now_add=True)),
                ('modifiedBy', models.CharField(max_length=255)),
                ('modifiedDate', models.DateField(auto_now=True)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Department.department')),
                ('designation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Designation.designation')),
            ],
        ),
        migrations.CreateModel(
            name='Applications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('applicant_name', models.CharField(max_length=255)),
                ('applicant_email', models.CharField(max_length=255)),
                ('applicant_phone', models.CharField(max_length=255)),
                ('applicant_status', models.CharField(max_length=255)),
                ('applicant_cv', models.CharField(max_length=255)),
                ('createdBy', models.CharField(max_length=255)),
                ('createdDate', models.DateField(auto_now_add=True)),
                ('modifiedBy', models.CharField(max_length=255)),
                ('modifiedDate', models.DateField(auto_now=True)),
                ('vacancy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Recruitment.vacancy')),
            ],
        ),
    ]
