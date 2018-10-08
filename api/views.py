from trading_simulator.models import account, coin, balance, tradeHistory
from .serializers import AccountSerializer, CoinSerializer, BalanceSerializer, TradeHistorySerializer
from rest_framework import viewsets
from django.http import JsonResponse

# Create your views here.
class AccountViewSet(viewsets.ModelViewSet):
    queryset = account.objects.all()
    serializer_class = AccountSerializer

class CoinViewSet(viewsets.ModelViewSet):
    queryset = coin.objects.all()
    serializer_class = CoinSerializer

class BalanceViewSet(viewsets.ModelViewSet):
    queryset = balance.objects.all()
    serializer_class = BalanceSerializer

class TradeHistoryViewSet(viewsets.ModelViewSet):
    queryset = tradeHistory.objects.all()
    serializer_class = TradeHistorySerializer