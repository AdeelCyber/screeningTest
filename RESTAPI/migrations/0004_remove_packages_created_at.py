# Generated by Django 3.2.19 on 2023-09-14 10:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('RESTAPI', '0003_applicationusers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='packages',
            name='created_at',
        ),
    ]
