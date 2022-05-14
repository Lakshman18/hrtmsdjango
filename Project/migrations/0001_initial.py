# Generated by Django 4.0.3 on 2022-04-02 15:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Client', '0002_rename_status_client_password_client_isactive_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('projectName', models.CharField(max_length=255)),
                ('startDate', models.DateField()),
                ('renewalDate', models.DateField()),
                ('isActive', models.BooleanField(default=True)),
                ('createdBy', models.CharField(max_length=255)),
                ('createdDate', models.DateField(auto_now_add=True)),
                ('modifiedBy', models.CharField(max_length=255)),
                ('modifiedDate', models.DateField(auto_now=True)),
                ('clientName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Client.client')),
                ('employee', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]