# Generated by Django 3.2.5 on 2021-08-02 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leavemanagementsys', '0002_leaverequest_applied_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='leaverequest',
            name='remark',
            field=models.CharField(default='NIL', max_length=50),
        ),
    ]