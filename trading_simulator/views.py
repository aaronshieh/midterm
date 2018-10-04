from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from trading_simulator.models import account, balance, tradeHistory, coin
from django.core import serializers
from bs4 import BeautifulSoup
import datetime, requests, json

# Create your views here.
def index(request):
    return render(request, 'trading_simulator/index.html')

def create(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        initial = float(request.POST['initial'])

        account.objects.create(name=name, email=email, password=password, initialAmount=initial)
        balance.objects.create(accountId=account.objects.get(email=email),
                                coinId=coin.objects.get(coinId=1),
                                coinBalance=initial)
        
        return redirect('/trading_simulator/login/')

    return render(request, 'trading_simulator/create.html')

def validateEmail(request):
    if request.method == 'GET':
        email = request.GET['email']
        email_in_db = serializers.serialize("json", account.objects.filter(email=email))
    return HttpResponse(email_in_db, content_type="application/json")

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

            response = HttpResponse('login success...<script>location.href="/trading_simulator/balances/{}"</script>'.format(account__.accountId))
            response.set_cookie("email", email)
            response.set_cookie("accountId", account__.accountId)
            return response

        else:
            # login fail
            print('fail')
            return HttpResponse('<script>alert("login failed...try again");location.href="/trading_simulator/login/";</script>')

    return render(request, 'trading_simulator/login.html')

def balances(request, id):
    if 'id' in request.session:
        accountId = request.session['id']

        account_ = account.objects.get(accountId=id)
        balance_ = balance.objects.filter(accountId=id)
        coin_ = coin.objects.all()
        tradeHistory_ = tradeHistory.objects.filter(accountId=id)

        return render(request, 'trading_simulator/showbalance.html', locals())
    else:
        return redirect('/trading_simulator/login/')

def trading(request, id):
    if 'id' in request.session:
        return render(request, 'trading_simulator/trade.html', locals())
    else:
        return redirect('/trading_simulator/login/')

def trade(request):
    if request.method == 'POST':
        accountId = request.session['id']
        price = request.POST['price']
        amount = request.POST['amount']
        type_ = request.POST['type']
        coinId = request.POST['coinId']

        print("PRICE = " + price)
        print("AMOUNT = " + amount)
        print("ACCOUNT ID = " + "{}".format(accountId))
        print("TYPE = " + type_)
        print("COIN ID = " + coinId)

        usd_balance = balance.objects.filter(accountId=accountId).get(coinId=1)
        coin_balance = balance.objects.filter(accountId=accountId).filter(coinId=coinId)
        total = float(price) * float(amount)

        successfulTransaction = False

        if coin_balance:
            print("already have this coin")
            
            if type_.lower() == 'buy':
                if total <= usd_balance.coinBalance and total > 0:
                    print("have enough money to buy: " + str(usd_balance.coinBalance))
                    usd_balance.coinBalance -= float(total)
                    coin_balance[0].coinBalance += float(amount)
                    print("new usd balance: " + str(usd_balance.coinBalance))
                    print("new coin balance: " + str(coin_balance[0].coinBalance))
                    successfulTransaction = True

            elif type_.lower() == 'sell':
                print("have enough to sell: " + str(coin_balance[0].coinBalance))
                if 0 < float(amount) <= coin_balance[0].coinBalance:
                    coin_balance[0].coinBalance -= float(amount)
                    usd_balance.coinBalance += total
                    print("new usd balance: " + str(usd_balance.coinBalance))
                    print("new coin balance: " + str(coin_balance[0].coinBalance))
                    successfulTransaction = True

            usd_balance.save()
            coin_balance[0].save()
            
        else:
            print("don't have this coin")

            if type_.lower() == 'buy':
                if total <= usd_balance.coinBalance and total > 0:
                    print("have enough money to buy: " + str(usd_balance.coinBalance))
                    usd_balance.coinBalance -= float(total)
                    balance.objects.create(accountId=account.objects.get(accountId=accountId),
                                            coinId=coin.objects.get(coinId=coinId),
                                            coinBalance=amount)
                    successfulTransaction = True
                    usd_balance.save()

        # write to trade history table
        if successfulTransaction:
            print("writing to trade history...")
            tradeHistory.objects.create(tradeType=type_,
                                    amount=float(amount),
                                    price=float(price),
                                    date=datetime.datetime.now(),
                                    accountId=account.objects.get(accountId=accountId),
                                    coinId=coin.objects.get(coinId=coinId))

            response = HttpResponse('success')

        else:
            response = HttpResponse('failed')

        return response

def logout(request):
    response = HttpResponse("<script>location.href='/trading_simulator/'</script>")
    response.delete_cookie('accountId')
    response.delete_cookie('email')
    
    request.session.clear()

    return response

def getBalance(request):
    accountId = request.session['id']
    balance_ = serializers.serialize("json", balance.objects.filter(accountId=accountId).exclude(coinBalance=0))
    account_ = serializers.serialize("json", account.objects.filter(accountId=accountId))
    tradeHistory_ = serializers.serialize("json", tradeHistory.objects.filter(accountId=accountId))

    data = {'account':json.loads(account_), 
            'balances':json.loads(balance_), 
            'trades':json.loads(tradeHistory_)}
    datastr = json.dumps(data)

    return HttpResponse(datastr, content_type="application/json")

def getCoins(request):
    coin_ = serializers.serialize("json", coin.objects.all())

    return HttpResponse(coin_, content_type="application/json")

def getCoinBalance(request, coinId):
    accountId = request.session['id']
    balance_ = serializers.serialize("json", balance.objects.filter(accountId=accountId).filter(coinId=coinId))
    return HttpResponse(balance_, content_type="application/json")

def getCMCcoin(request):
    if request.method == 'GET':
        ticker = request.GET['ticker']
        request_url = 'https://api.coinmarketcap.com/v2/ticker/' + ticker +'/'
        r = requests.get(request_url)
        
        return JsonResponse(r.json())

def getCryptoNews(request):
    url = 'https://www.ccn.com/'

    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    }

    response = requests.get(url, headers=header)
    soup = BeautifulSoup(response.text, "lxml")

    article_list = []
    articles = soup.select('.page-content .posts-row article')
    for article in articles:
        article_title = article.find('header').find('h4', class_="entry-title").find('a').string
        article_link = article.find('header').find('h4', class_="entry-title").find('a').get('href')
        article_image = article.find('div', class_='post-thumbnail').find('img').get('src')
        article_date = article.find('header').find(class_="updated").get('datetime')
        article_list.append({"title":article_title, "link":article_link, "img":article_image, "time":article_date})
        # print(article_title)
        # print(article_link)
        # print(article_image)
        # print(article_date)
        # print('')

    articles_ = {"articles":article_list}
    # articles_ = json.dumps(articles_)
    # print(articles_)
    return JsonResponse(articles_)