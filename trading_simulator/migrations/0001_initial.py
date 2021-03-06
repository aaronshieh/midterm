# Generated by Django 2.1.1 on 2018-09-25 12:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='account',
            fields=[
                ('accountId', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=40)),
                ('initialAmount', models.FloatField(default=0)),
            ],
            options={
                'db_table': 'accounts',
            },
        ),
        migrations.CreateModel(
            name='balance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coinBalance', models.FloatField()),
                ('accountId', models.ForeignKey(db_column='accountId', on_delete=django.db.models.deletion.CASCADE, to='trading_simulator.account')),
            ],
            options={
                'db_table': 'balances',
            },
        ),
        migrations.CreateModel(
            name='coin',
            fields=[
                ('coinId', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('symbol', models.CharField(max_length=10)),
                ('cmcId', models.IntegerField()),
            ],
            options={
                'db_table': 'coins',
            },
        ),
        migrations.CreateModel(
            name='tradeHistory',
            fields=[
                ('tradeId', models.AutoField(primary_key=True, serialize=False)),
                ('tradeType', models.CharField(max_length=10)),
                ('amount', models.FloatField()),
                ('price', models.FloatField()),
                ('date', models.DateTimeField()),
                ('accountId', models.ForeignKey(db_column='accountId', on_delete=django.db.models.deletion.CASCADE, to='trading_simulator.account')),
                ('coinId', models.ForeignKey(db_column='coinId', on_delete=django.db.models.deletion.CASCADE, to='trading_simulator.coin')),
            ],
            options={
                'db_table': 'trade_history',
            },
        ),
        migrations.AddField(
            model_name='balance',
            name='coinId',
            field=models.ForeignKey(db_column='coinId', on_delete=django.db.models.deletion.CASCADE, to='trading_simulator.coin'),
        ),
        migrations.AlterUniqueTogether(
            name='balance',
            unique_together={('accountId', 'coinId')},
        ),
    ]
