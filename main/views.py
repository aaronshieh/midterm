from django.shortcuts import render

def index(request):
    title = "Welcome to finAI!"
    return render(request, 'index.html', locals())