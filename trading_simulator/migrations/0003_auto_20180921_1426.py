# Generated by Django 2.1.1 on 2018-09-21 06:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trading_simulator', '0002_auto_20180921_1420'),
    ]

    operations = [
        migrations.RenameField(
            model_name='balance',
            old_name='balance',
            new_name='coinBalance',
        ),
    ]
