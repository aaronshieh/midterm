from django.db import models

# Create your models here.
class account(models.Model):
    accountId = models.AutoField(primary_key=True)
    email = models.EmailField()
    password = models.CharField(max_length=20)
    name = models.CharField(max_length=40)
    initialAmount = models.FloatField(default=0)

    class Meta:
        db_table = 'accounts'

class coin(models.Model):
    coinId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    symbol = models.CharField(max_length=10)

    class Meta:
        db_table = 'coins'

class balance(models.Model):
    accountId = models.ForeignKey(account,models.DO_NOTHING,primary_key=True,db_column='accountId')
    USDbalance = models.FloatField()
    BTCbalance = models.FloatField(blank=True, null=True)
    ETHbalance = models.FloatField(blank=True, null=True)
    EOSbalance = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = 'balances'

class tradeHistory(models.Model):
    tradeId = models.AutoField(primary_key=True)
    coinId = models.ForeignKey(coin,models.DO_NOTHING,db_column='coinId')
    accountId = models.ForeignKey(account,models.DO_NOTHING,db_column='accountId')
    tradeType = models.CharField(max_length=10)
    amount = models.FloatField()
    price = models.FloatField()
    date = models.DateTimeField()

    class Meta:
        db_table = 'trade_history'