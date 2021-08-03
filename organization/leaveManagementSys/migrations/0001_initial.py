# Generated by Django 3.2.5 on 2021-08-03 07:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LeaveRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('from_date', models.DateField(default=django.utils.timezone.now, unique=True)),
                ('to_date', models.DateField(default=django.utils.timezone.now, unique=True)),
                ('leave_type', models.CharField(default='Personal', max_length=10)),
                ('number_of_days', models.IntegerField()),
                ('status', models.CharField(default='Pending', max_length=10)),
                ('remark', models.CharField(default='NIL', max_length=50)),
            ],
        ),
    ]
