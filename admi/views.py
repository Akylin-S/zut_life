from datetime import date

from django.shortcuts import render, redirect

from django.views import View

# Create your views here.
from account.models import UserInfo
from admi.models import BackUser
from admi.utils.visit_count import five_visit, visit_count
from function.models import Topic, Reply, scenery, l_reply, lost, confession, c_reply
import json

class login(View):
    def get(self, request):
        if request.COOKIES.get("is_login_back"):
            return redirect('/admi/home/')
        num = BackUser.objects.filter().count()
        if num == 0:
            BackUser.objects.create(back_user='kylin',back_password=123456)
        return render(request, 'admi/admin_login.html')

    def post(self, request):
        if request.COOKIES.get("is_login_back"):
            return redirect('/admi/home/')
        user = request.POST.get('username')
        password = request.POST.get('password')
        message = "账户或密码错误"
        try:
            dbuser = BackUser.objects.get(back_user=user)
        except:
            dbuser = None
        if dbuser == None:
            message = "账户或密码错误"
            return render(request, 'admi/admin_login.html', {"message": message})
        if dbuser.back_password == password:
            rep = redirect('/admi/home/')
            rep.set_cookie("is_login_back", True)
            rep.set_cookie('user', user)
            rep.set_cookie('password', password)
            return rep
        return render(request, 'admi/admin_login.html', {"message": message})


class home(View):

    def get(self, request):
        if not request.COOKIES.get("is_login_back"):
            return redirect('/admi/login/')
        user = request.COOKIES.get("back_user")
        user_num = UserInfo.objects.all().count()
        fiveday_visit_num = five_visit(request)
        visit_now = visit_count(request)

        publish_num = Topic.objects.filter(create_time=date.today()).count()
        forum_num = Topic.objects.all().count()
        con_num = confession.objects.all().count()
        lost_num = lost.objects.all().count()
        context = {
            'post_num': publish_num,
            'back_user': user,
            'visit': visit_now,
            'user_num': user_num,
            'five_day_visit': fiveday_visit_num,
            'forum_num': forum_num,
            'con_num': con_num,
            'lost_num': lost_num,
        }
        return render(request, 'admi/home.html', context)


class user_admin(View):
    def get(self, request):
        if not request.COOKIES.get("is_login_back"):
            return redirect('/admi/login/')
        user = UserInfo.objects.all()
        response = {
            'user_info': user
        }
        return render(request, 'admi/user.html', response)

    def post(self, request):
        if not request.COOKIES.get("is_login_back"):
            return redirect('/admi/login/')
        id = request.POST.get('id')

        user = UserInfo.objects.get(user_id=id)
        user.delete()
        user = UserInfo.objects.all()
        response = {
            'user_info': user
        }
        return render(request, 'admi/user.html', response)


class forum_admin(View):
    def get(self, request):
        if not request.COOKIES.get("is_login_back"):
            return redirect('/admi/login/')

        forum = Topic.objects.all()
        response = {
            'topic': forum
        }
        return render(request, 'admi/forum.html', response)

    def post(self, request):
        if not request.COOKIES.get("is_login_back"):
            return redirect('/admi/login/')
        id = request.POST.get('id')
        forum = Topic.objects.get(id=id)
        forum.delete()
        reply = Reply.objects.filter(r_tid=id)
        reply.delete()
        forum = Topic.objects.all()
        response = {
            'topic': forum
        }
        return render(request, 'admi/forum.html', response)

class confession_admin(View):
    def get(self, request):
        if not request.COOKIES.get("is_login_back"):
            return redirect('/admi/login/')

        con = confession.objects.all()
        response = {
            'confession': con
        }
        return render(request, 'admi/confession.html', response)

    def post(self, request):
        if not request.COOKIES.get("is_login_back"):
            return redirect('/admi/login/')
        id = request.POST.get('id')
        con = confession.objects.get(id=id)
        con.delete()
        reply = c_reply.objects.filter(c_tid=id)
        reply.delete()
        con = confession.objects.all()
        response = {
            'confession': con
        }
        return render(request, 'admi/confession.html', response)

class lost_admin(View):
    def get(self, request):
        if not request.COOKIES.get("is_login_back"):
            return redirect('/admi/login/')

        lost1 = lost.objects.all()
        response = {
            'lost': lost1
        }
        return render(request, 'admi/lost.html', response)

    def post(self, request):
        if not request.COOKIES.get("is_login_back"):
            return redirect('/admi/login/')
        id = request.POST.get('id')
        lost1 = lost.objects.get(id=id)
        lost1.delete()
        reply = l_reply.objects.filter(l_tid=id)
        reply.delete()
        lost1 = lost.objects.all()
        response = {
            'lost': lost1
        }
        return render(request, 'admi/lost.html', response)

class admin_scenery(View):

    def get(self, request):
        if not request.COOKIES.get("is_login_back"):
            return redirect('/admi/login/')
        r_scenery = scenery.objects.filter(s_pass='2')
        n_scenery = scenery.objects.filter(s_pass='0')
        p_scenery = scenery.objects.filter(s_pass='1')
        response = {
            'r_scenery': r_scenery,
            'n_scenery': n_scenery,
            'p_scenery': p_scenery
        }
        return render(request, 'admi/scenery.html', response)

    def post(self, request):
        if not request.COOKIES.get("is_login_back"):
            return redirect('/admi/login/')
        id = request.POST.get('id')
        s_pass = request.POST.get('pass')
        if s_pass == '1' :

            sc =scenery.objects.get(id=id)
            sc.s_pass =str(s_pass)
            sc.save()
        elif s_pass == '0':
            print(s_pass)
            sc = scenery.objects.get(id=id)
            sc.s_pass = str(s_pass)
            sc.save()
        elif s_pass=='3':
            print(s_pass)
            sc =scenery.objects.get(id=id)
            sc.delete()

        r_scenery = scenery.objects.filter(s_pass='2')
        n_scenery = scenery.objects.filter(s_pass='0')
        p_scenery = scenery.objects.filter(s_pass='1')
        response = {
            'r_scenery': r_scenery,
            'n_scenery': n_scenery,
            'p_scenery': p_scenery
        }
        return render(request, 'admi/scenery.html', response)

def logout(request):
    if not request.COOKIES.get("is_login_back"):
        return redirect('/admi/login/')
    rep = redirect('/admi/login/')
    rep.delete_cookie('is_login_back')
    rep.delete_cookie('user')
    rep.delete_cookie('password')
    return rep
