# Generated by Django 3.2.19 on 2023-09-14 10:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('RESTAPI', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Packages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.FloatField()),
                ('userAllowed', models.IntegerField()),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='users',
            name='roles',
            field=models.CharField(choices=[('SUPER_ADMIN', 'Super Admin'), ('USER', 'User')], default='USER', max_length=100),
        ),
        migrations.CreateModel(
            name='Subscriptions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('application', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='RESTAPI.application')),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RESTAPI.packages')),
            ],
        ),
    ]
