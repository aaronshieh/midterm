from trading_simulator.models import account, coin, balance, tradeHistory
from .serializers import AccountSerializer, CoinSerializer, BalanceSerializer, TradeHistorySerializer
from rest_framework import viewsets
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

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
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_fields = '__all__'
    ordering_fields = '__all__'
    def get_queryset(self):
        queryset = balance.objects.all()
        cmcId = self.request.query_params.get('cmcId', None)
        if cmcId is not None:
            return queryset.filter(coinId__cmcId=cmcId)
        else:
            return queryset

class TradeHistoryViewSet(viewsets.ModelViewSet):
    queryset = tradeHistory.objects.all()
    serializer_class = TradeHistorySerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_fields = '__all__'
    ordering_fields = '__all__'