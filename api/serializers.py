from rest_framework import serializers
from trading_simulator.models import account, coin, balance, tradeHistory

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = account
        fields = '__all__'

class CoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = coin
        fields = '__all__'

class BalanceSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='coinId.name')
    symbol = serializers.ReadOnlyField(source='coinId.symbol')
    cmcId = serializers.ReadOnlyField(source='coinId.cmcId')

    class Meta:
        model = balance
        fields = ('accountId', 'name', 'symbol', 'coinBalance', 'cmcId')

class TradeHistorySerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='coinId.name')
    symbol = serializers.ReadOnlyField(source='coinId.symbol')

    class Meta:
        model = tradeHistory
        fields = '__all__'