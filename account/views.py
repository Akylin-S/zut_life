from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.template import loader
from django.views import View
from django_redis import get_redis_connection

from .captcha.captcha import captcha
from account.models import UserInfo
from . import constants


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
        print(6)
        return render(request, 'account/login.html')

    def post(self, request):
        print(2)
        if request.COOKIES.get('is_login'):
            return redirect('')
        json = request.POST
        user = json['username']
        print(user)
        password = json['password']
        message = '账号不存在'
        try:
            dbuser = UserInfo.objects.get(user=user)
            print(dbuser.user)
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
        print(4)
        return redirect('/index/success/')
    return render(request, 'account/login.html')


class Verification_Register(View):

    def get(self, request):
        print(33)
        return render(request, 'account/register.html')

    def post(self, request):
        print(3)
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
    print(1)
    # template = loader.get_template('account/register.html')
    return render(request, 'account/register.html')


def have_login(request):
    return render(request, 'account/success.html')
