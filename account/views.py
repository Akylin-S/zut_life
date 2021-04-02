import os

from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.template import loader
from django.views import View
from django_redis import get_redis_connection

from .captcha.captcha import captcha
from account.models import UserInfo
from . import constants
from account.untils.account import day_visit

class ImageCodeView(View):
    """
    图片验证码
    """

    def get(self, request, image_code_id):
        """
        获取图片验证码
        """
        # 生成验证码图片
        text, image = captcha.generate_captcha()
        redis_conn = get_redis_connection("verify_codes")
        redis_conn.setex("img_%s" % image_code_id, constants.IMAGE_CODE_REDIS_EXPIRES, text)
        # 固定返回验证码图片数据，不需要REST framework框架的Response帮助我们决定返回响应数据的格式
        # 所以此处直接使用Django原生的HttpResponse即可
        return HttpResponse(image, content_type="images/jpg")


class verifications(View):
    def get(self, request):
        return render(request, 'account/login.html')

    def post(self, request):
        if request.COOKIES.get('is_login'):
            return redirect('')
        json = request.POST
        user = json['username']
        password = json['password']
        message = '账号不存在'
        try:
            dbuser = UserInfo.objects.get(user=user)
        except:
            print('error')
            return render(request, 'account/login.html', {"message": message})
        if dbuser.password == password:
            rep = redirect('/index/success/')
            rep.set_cookie("is_login", True)
            username = dbuser.user
            userid = dbuser.user_id
            userimg = dbuser.user_img
            rep.set_cookie("user_name", username)
            rep.set_cookie("user_id", userid)
            rep.set_cookie("user_img", userimg)
            request.session["user"] = username
            return rep
        else:
            return render(request, 'account/login.html', {"message": '账号或密码错误'})


def login(request):
    if request.COOKIES.get("is_login"):
        return redirect('/index/success/')
    day_visit(request)
    return render(request, 'account/login.html')


class Verification_Register(View):

    def get(self, request):
        return render(request, 'account/register.html')

    def post(self, request):
        user = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmpassword')
        text1 = request.POST.get('verift')
        uuid = request.POST.get('img_code')
        print(uuid)
        redis_conn = get_redis_connection("verify_codes")
        text2 = redis_conn.get("img_%s" % uuid).decode()
        if text2.lower() != text1.lower():
            message = '验证码错误'
            return render(request, 'account/register.html', {'message': message})

        if password == confirm_password:
            user_name = UserInfo.objects.filter(user=user)
            if user_name:
                message = '用户名已存在'
                return render(request, 'account/register.html', {'message': message})
            user = UserInfo(user=user, password=password)
            user.save()
            return redirect('/account/login/')
        message = '两次密码不相同'
        return render(request, 'account/register.html', {'message': message})


def register(request):
    # template = loader.get_template('account/register.html')
    return render(request, 'account/register.html')


def logout(request):
    rep = redirect('/account/login/')
    rep.delete_cookie("is_login")
    rep.delete_cookie('user_id')
    rep.delete_cookie('user_name')
    rep.delete_cookie('user_img')
    return rep


def persron_center(request):
    if not request.COOKIES.get("is_login"):
        return redirect('/account/login/')
    user = request.COOKIES.get("user_name")
    dbuser = UserInfo.objects.get(user=user)

    # confession_list = PostInfo.objects.filter(category="confession",reviewed="past")
    template = loader.get_template('account/personal_center.html')
    context = {
        "user": dbuser,
    }
    return HttpResponse(template.render(context))


class change(View):

    def get(self, request):
        print(1)
        return redirect('/account/personal_center/')

    def post(self, request):
        print(5)
        if not request.COOKIES.get('is_login'):
            return redirect('/account/login/')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')
        print(password1)
        print(password)
        user = request.COOKIES.get("user_name")
        dbuser = UserInfo.objects.get(user=user)
        if password == password1:
            print(7)
            dbuser.password = password
            dbuser.save()
            return redirect('/account/logout/')
        else:
            print(8)
            return render(request, 'account/personal_center.html', {"user": dbuser, "message_password": '两次输入的密码不同'})


class setting(View):

    def get(self, request):
        return redirect('/account/personal_center/')

    def post(self, request):
        if not request.COOKIES.get('is_login'):
            return redirect('/account/login/')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        user_img = request.FILES.get('img')
        user = request.COOKIES.get("user_name")
        dbuser = UserInfo.objects.get(user=user)
        dbuser.email = email
        dbuser.phone = phone
        dbuser.user_img = user_img
        dbuser.save()

class ChangeUserData(View):
    def get(self, request):
        return redirect('/account/personal_center/')

    def post(self,request):
        if not request.COOKIES.get("is_login"):
            return redirect('/account/login')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        gender = request.POST['selected']
        img = request.FILES.get('img')
        print(type(str(img)))
        user = request.COOKIES.get("user_name")
        dbuser = UserInfo.objects.get(user=user)
        if email:
            dbuser.email=email
        if img:
            mk ='static/img/user_img/'+str(user)
            if not os.path.exists(mk):
                os.mkdir(mk)
            user_img = 'static/img/user_img/'+str(user)+'/'+str(img)
            print(user_img)
            f = open(os.path.join(user_img),'wb')
            for line in img.chunks():
                f.write(line)
            f.close()
            dbuser.user_img=user_img
        if phone:
            dbuser.phone=phone
        dbuser.gender=gender
        dbuser.save()
        # phone = json['phone']
        # user_img = request.FILES.get('img')
        # print(user_img)
        # email = json['email']
        # user_id = request.COOKIES.get("user_id")
        # dbuser = UserInfo.objects.get(user_id=user_id)
        # dbuser.phone = phone
        # dbuser.email = email
        # dbuser.user_img = user_img
        # dbuser.save()
        return redirect('/account/personal_center/')
