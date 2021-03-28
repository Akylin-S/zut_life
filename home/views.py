from django.shortcuts import render, redirect

# Create your views here.
from django.views import View


def index(request):
    if request.COOKIES.get("is_login"):
        return redirect('/index/success/')
    return render(request, 'home/home.html')
