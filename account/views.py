from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.template import loader
from django.views import View

from account.models import UserInfo


class verifications(View):
    def get(self,request):
        print(77777777777)

    def post(self, request):
        # if request.COOKIES.get('is_login'):
        #     return redirect('')
        json = request.POST
        user = json['username']
        password = json['password']
        message = '账号不存在或账号密码错误'
        print(user)
        # try:
        #     dbuser = UserInfo.objects.get(user=user)
        # except:
        #     print('失败')
        #     return render(request, 'account/login.html', {'message': message})
        # else:
        #     if dbuser.password == password:
        #         rep = redirect('/loss/')
        #
        return render(request, '/account/login.html')

def login(request):
    if request.COOKIES.get("is_login"):
        return redirect('/forum/templates/forum/Confession.html')
    template = loader.get_template('account/login.html')
    context = {}
    return HttpResponse(template.render(context, request))
