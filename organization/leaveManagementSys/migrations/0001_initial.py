# Generated by Django 3.2.5 on 2021-08-01 15:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LeaveRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('from_date', models.DateField(default=django.utils.timezone.now)),
                ('to_date', models.DateField(default=django.utils.timezone.now)),
                ('Leave_type', models.CharField(max_length=100)),
                ('number_of_days', models.IntegerField()),
                ('applied_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
