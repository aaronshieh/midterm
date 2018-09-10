from django.shortcuts import render, redirect
from django.db import connection

def index(request):
    with connection.cursor() as cursor:
        sql = "select * from accounts"
        cursor.execute(sql)
        accounts = cursor.fetchall()
    return render(request, 'account/index.html', locals())

def new_account(request):
    if request.method == "POST":
        name = request.POST['name']
        balance = request.POST['balance']

        with connection.cursor() as cursor:
            sql = "insert into accounts(name, balance) values(%s, %s)"
            cursor.execute(sql, (name, balance))
        return redirect('/account/')

    return render(request, 'account/new.html', locals())

def delete(request, id):
    with connection.cursor() as cursor:
        sql = "delete from accounts where id=%s"
        cursor.execute(sql, (id,))
    return redirect('/account/')

def edit(request, id):
    if request.method == "POST":
        name = request.POST['name']

        with connection.cursor() as cursor:
            sql = "update accounts set name=%s where id=%s"
            cursor.execute(sql, (name, id))
        
        return redirect('/account/')

    with connection.cursor() as cursor:
        sql = "select * from accounts where id=%s"
        cursor.execute(sql, (id,))
        accounts = cursor.fetchone()
    return render(request, 'account/edit.html', locals())

def deposit(request, id):
    if request.method == "POST":
        deposit = request.POST['deposit']

        with connection.cursor() as cursor:
            sql = "select balance from accounts where id=%s"
            cursor.execute(sql, (id,))
            accounts = cursor.fetchone()
            
            new_balance = accounts[0] + int(deposit)
            sql = "update accounts set balance=%s where id=%s"
            cursor.execute(sql, (new_balance, id))

        return redirect('/account/')

    return render(request, 'account/deposit.html', locals())