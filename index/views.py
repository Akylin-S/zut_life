from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.template import loader
from django.views import View

from account.models import UserInfo


class Confession(View):

    def get(self,request):

        if not request.COOKIES.get("is_login"):
            return redirect('/account/login')
        # 访问量
        # day_visit(request)

        user = request.COOKIES.get("user_name")
        dbuser = UserInfo.objects.get(user=user)

        # confession_list = PostInfo.objects.filter(category="confession",reviewed="past")
        template = loader.get_template('index/index.html')
        context = {
            "user":dbuser,
        }
        return HttpResponse(template.render(context))

