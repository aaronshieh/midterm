from django.urls import path
from . import views

app_name = "trading_simulator"

urlpatterns = [
    path('', views.index, name="index"),
    path('create/', views.create, name="create"),
    path('deposit/<int:id>', views.deposit, name="deposit"),
    path('login/', views.login, name="login"),
    path('balances/<int:id>', views.balances, name="balances"),
    path('trading/<int:id>', views.trading, name="trading"),
    path('trade/', views.trade),
    path('logout/', views.logout),
    path('getBalance/', views.getBalance),
    path('getCoins/', views.getCoins),
    path('getCoinBalance/<int:coinId>/', views.getCoinBalance),
    path('getCMCcoin/', views.getCMCcoin)
]