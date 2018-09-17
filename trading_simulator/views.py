from django.shortcuts import render, redirect
from django.http import HttpResponse
from trading_simulator.models import account, balance, tradeHistory, coin
from django.core import serializers
import datetime

# Create your views here.
def index(request):
    return render(request, 'trading_simulator/index.html')

def create(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        initial = request.POST['initial']

        account.objects.create(name=name, email=email, password=password, initialAmount=initial)
        balance.objects.create(accountId=account.objects.get(email=email),
                                USDbalance=initial,
                                BTCbalance=0.0,
                                ETHbalance=0.0,
                                EOSbalance=0.0)

    return render(request, 'trading_simulator/create.html')

def deposit(request, id):
    balance_ = balance.objects.get(accountId=id)

    if request.method == 'POST':
        USDbalance = request.POST['usd']
        BTCbalance = request.POST['btc']

        balance_.USDbalance = USDbalance
        balance_.BTCbalance = BTCbalance
        balance_.save()

        return redirect('/')

    return render(request, 'trading_simulator/deposit.html', locals())

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        account_ = account.objects.filter(email=email, password=password)

        if account_:
            # login success
            print('success')
            account__ = account.objects.get(email=email, password=password)

            # session
            request.session['id'] = account__.accountId

            response = HttpResponse('login sucess...<script>location.href="/"</script>')
            response.set_cookie("email", email)
            response.set_cookie("accountId", account__.accountId)
            return response

        else:
            # login fail
            print('fail')
            return redirect('/')

    return render(request, 'trading_simulator/login.html')

def balances(request, id):
    account_ = account.objects.get(accountId=id)
    balance_ = balance.objects.get(accountId=id)
    tradeHistory_ = tradeHistory.objects.filter(accountId=id)

    return render(request, 'trading_simulator/showbalance.html', locals())

def trading(request, id):
    return render(request, 'trading_simulator/trade.html', locals())

def trade(request):
    if request.method == 'POST':
        accountId = request.session['id']
        price = request.POST['price']
        amount = request.POST['amount']
        type_ = request.POST['type']
        currency = request.POST['currency']

        print("PRICE = " + price)
        print("AMOUNT = " + amount)
        print("ACCOUNT ID = " + "{}".format(accountId))
        print("TYPE = " + type_)
        print("CURRENCY = " + currency)

        account_ = account.objects.get(accountId=accountId)
        balance_ = balance.objects.get(accountId=accountId)

        successfulTransaction = False

        if type_ == 'buy':
            total = float(price) * float(amount)
            if total <= balance_.USDbalance and total > 0:
                balance_.USDbalance -= total
                successfulTransaction = True
                if currency == 'btc':
                    balance_.BTCbalance += float(amount)
                elif currency == 'eth':
                    balance_.ETHbalance += float(amount)
                elif currency == 'eos':
                    balance_.EOSbalance += float(amount)
            balance_.save()
        
        elif type_ == 'sell':
            total = float(price) * float(amount)
            if currency == 'btc':
                if 0 < float(amount) <= balance_.BTCbalance:
                    balance_.BTCbalance -= float(amount)
                    balance_.USDbalance += total
                    successfulTransaction = True
            elif currency == 'eth':
                if 0 < float(amount) <= balance_.ETHbalance:
                    balance_.ETHbalance -= float(amount)
                    balance_.USDbalance += total
                    successfulTransaction = True
            elif currency == 'eos':
                if 0 < float(amount) <= balance_.EOSbalance:
                    balance_.EOSbalance -= float(amount)
                    balance_.USDbalance += total
                    successfulTransaction = True
            balance_.save()

        # write to trade history table
        if successfulTransaction:
            print("writing to trade history...")
            tradeHistory.objects.create(tradeType=type_,
                                    amount=float(amount),
                                    price=float(price),
                                    date=datetime.datetime.now(),
                                    accountId=account.objects.get(accountId=accountId),
                                    coinId=coin.objects.get(symbol=currency))

        response = HttpResponse('success')
        return response

def logout(request):
    response = HttpResponse("<script>location.href='/'</script>")
    response.delete_cookie('accountId')
    response.delete_cookie('email')
    
    request.session.clear()

    return response

def getBalance(request):
    accountId = request.session['id']
    balance_ = serializers.serialize("json",
                                    balance.objects.filter(accountId=accountId))

    return HttpResponse(balance_, content_type="application/json")