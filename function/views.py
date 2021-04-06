import json
import os

from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
# 校园论坛功能
from django.template import loader
from django.views import View

from account.models import UserInfo
from function.models import Topic, Reply, scenery, confession, c_images, c_reply, lost, l_images, l_reply


class forum(View):

    def get(self, request, kid, reply_limit, time_limit, page_number):
        if not request.COOKIES.get("is_login"):
            return redirect('/account/login')
        uid = request.COOKIES.get("user_id")
        dbuser = UserInfo.objects.get(user_id=uid)
        if kid == '0' and reply_limit == '0' and time_limit == '0':
            # 默认时间排序把帖子传过去
            topics = Topic.objects.filter()
        else:
            # request.path_info   # 获取当前url
            # from django.urls import reverse
            # reverse('all_tie', kwargs={'kid': '0', 'reply_limit': '0', 'time_limit': '0'})

            topics = Topic.objects.filter()

            # 筛选分类
            if kid != '0':
                topics = Topic.objects.filter(t_kind=kid)

            # 筛选回复数量
            tmp = []

            for topic in topics:
                # 查看每个帖子的回复数量
                count = len(Reply.objects.filter(r_tid=topic.id))

                if reply_limit == '0':
                    pass
                elif reply_limit == '1':  # 1是大于100
                    print('到1了')
                    if count < 100:
                        print('到了')
                        continue
                elif reply_limit == '2':  # 2是30-100
                    if count < 30 or count > 100:
                        continue
                elif reply_limit == '3':  # 3是小于30
                    if count > 30:
                        continue
                tmp.append(topic)
            topics = tmp

            # 筛选发布时间
            tmp = []
            for topic in topics:
                if time_limit == '0':  # 0是全部时间
                    pass
                elif time_limit == '1':  # 1是1个月内
                    # 如果在限制之前，就筛掉
                    pass
                elif time_limit == '2':  # 2是3个月内
                    # 如果在限制之前，就筛掉
                    pass
                elif time_limit == '3':  # 3是6个月内
                    # 如果在限制之前，就筛掉
                    pass
                elif time_limit == '4':  # 4是1年内
                    # 如果在限制之前，就筛掉
                    pass
                tmp.append(topic)
            topics = tmp
        paginator = Paginator(topics, 4)
        if paginator.num_pages >= int(page_number):
            page = paginator.page(int(page_number))
        else:
            page = paginator.page(paginator.num_pages)
        response = {
            'topics': page,
            'kid': kid,
            'time_limit': time_limit,
            'reply_limit': reply_limit,
            'uid': uid,
            'page': page,
            'paginator': paginator,
            'user': dbuser
        }
        return render(request, 'function/forum.html', response)

    def post(self, request, kid, reply_limit, time_limit, page_number):
        if not request.COOKIES.get("is_login"):
            return redirect('/account/login')
        uid = request.COOKIES.get("user_id")
        # 搜索接收一个字段，查询标题或者简介里有关键字的帖子
        dbuser = UserInfo.objects.get(user_id=uid)
        keys = request.POST.get('keys')
        if not keys:
            return redirect('/function/forum-0-0-0/1/')
        # 按关键字查询标题里含有关键字的
        if kid == '0' and reply_limit == '0' and time_limit == '0' and keys:
            # 默认时间排序把帖子传过去
            topics = Topic.objects.filter(t_title__icontains=keys)

        if kid != '0':
            topics = Topic.objects.filter(Q(t_title__icontains=keys) & Q(t_kind=kid))
            # 筛选回复数量
            tmp = []
            for topic in topics:
                # 查看每个帖子的回复数量
                count = len(Reply.objects.filter(r_tid=topic.id))

                if reply_limit == '0':
                    pass
                elif reply_limit == '1':  # 1是大于100
                    print('到1了')
                    if count < 100:
                        print('到了')
                        continue
                elif reply_limit == '2':  # 2是30-100
                    if count < 30 or count > 100:
                        continue
                elif reply_limit == '3':  # 3是小于30
                    if count > 30:
                        continue
                tmp.append(topic)
            topics = tmp

            # 筛选发布时间
            tmp = []
            for topic in topics:
                if time_limit == '0':  # 0是全部时间
                    pass
                elif time_limit == '1':  # 1是1个月内
                    # 如果在限制之前，就筛掉
                    pass
                elif time_limit == '2':  # 2是3个月内
                    # 如果在限制之前，就筛掉
                    pass
                elif time_limit == '3':  # 3是6个月内
                    # 如果在限制之前，就筛掉
                    pass
                elif time_limit == '4':  # 4是1年内
                    # 如果在限制之前，就筛掉
                    pass
                tmp.append(topic)
            topics = tmp
        paginator = Paginator(topics, 4)
        if paginator.num_pages >= int(page_number):
            page = paginator.page(int(page_number))
        else:
            page = paginator.page(paginator.num_pages)
        return render(request, 'function/forum.html', {
            'page': page,
            'kid': kid,
            'time_limit': time_limit,
            'reply_limit': reply_limit,
            'paginator': paginator,
            'topics': page,
            'uid': uid,
            'user': dbuser,
            'keys': keys
        }
                      )


def publish_forum(request):
    if not request.COOKIES.get("is_login"):
        return redirect('/account/login')
        # 访问量
        # day_visit(request)

    user = request.COOKIES.get("user_name")
    dbuser = UserInfo.objects.get(user=user)

    # confession_list = PostInfo.objects.filter(category="confession",reviewed="past")
    template = loader.get_template('function/publish_forum.html')
    context = {
        "user": dbuser,
    }
    return HttpResponse(template.render(context))


def to_publish_forum(request):
    if not request.COOKIES.get("is_login"):
        return redirect('/account/login')
    if request.method == 'POST':
        uid = request.COOKIES.get("user_id")
        # 提交发布的文章
        t_title = request.POST.get('t_title')
        t_introduce = request.POST.get('t_introduce')
        t_content = request.POST.get('t_content')
        t_kind = request.POST.get('t_kind')
        obj = Topic.objects.create(t_title=t_title, t_introduce=t_introduce,
                                   t_content=t_content, t_kind=t_kind, t_uid=uid)
        t_id = obj.id
        # 存帖子图片
        t_photo = request.FILES.get('t_photo')
        print(t_photo != None)


        if t_photo != None:
            print(6666666)
            # 保存文件
            t_photo_path = 'static/img/t_photo/' + str(t_id) + '_' + t_photo.name
            f = open(os.path.join(t_photo_path), 'wb')
            for line in t_photo.chunks():
                f.write(line)
            f.close()
            # 吧图片路径存入数据库
            Topic.objects.filter(id=t_id).update(t_photo='/' + t_photo_path)

        return redirect('/function/forum-0-0-0/1')


# 单个帖子页面
def single(request, tid):
    if not request.COOKIES.get("is_login"):
        return redirect('/account/login')
    if request.method == 'GET':
        # 帖子内容
        # 时间类别作者，标题，正文，图片path
        try:
            topic = Topic.objects.get(id=tid)
        except Exception as e:
            return redirect('/home')

        t_time = topic.create_time
        t_kind = topic.t_kind
        t_title = topic.t_title
        t_content = topic.t_content
        t_photo = topic.t_photo
        t_uid = topic.t_uid
        t_introduce = topic.t_introduce
        uid = request.COOKIES.get('user_id')
        dbuser = UserInfo.objects.get(user_id=uid)

        response = {
            'tid': tid,
            't_uid': t_uid,
            't_time': t_time,
            't_kind': t_kind,
            't_title': t_title,
            't_content': t_content,
            't_photo': t_photo,
            't_introduce': t_introduce,
            'uid': uid,
            'user': dbuser,
        }

        # 留言内容
        # 留言者，留言时间，留言内容
        replys = Reply.objects.filter(r_tid=tid)
        reply_list = []
        for reply in replys:
            single_reply = {
                'r_uid': reply.r_uid,
                'r_time': reply.r_time,
                'r_content': reply.r_content,
                'r_id': reply.id,
                'r_photo': reply.r_photo,
            }
            reply_list.append(single_reply)
        response['reply_list'] = reply_list

        return render(request, 'function/detail_forum.html', response)

    elif request.method == 'POST':
        # 判断是否登录
        uid = request.COOKIES.get('user_name')
        if not uid:
            return redirect('/account/login')
        # 进行回复
        r_content = request.POST.get('r_content')
        if not r_content:
            return redirect('/function/single/' + tid)
        # 提交数据库
        obj = Reply.objects.create(r_tid=tid, r_uid=uid, r_content=r_content)

        r_id = str(obj.id)
        r_photo = request.FILES.get('r_photo')
        r_photo_path = ''
        if r_photo:
            # 保存文件
            r_photo_path = 'static/img/r_photo/' + r_id + '_' + r_photo.name
            f = open(os.path.join(r_photo_path), 'wb')
            for line in r_photo.chunks():
                f.write(line)
            f.close()

        # 吧图片路径存入数据库
        Reply.objects.filter(id=r_id).update(r_photo='/' + r_photo_path)
        return redirect('/function/single/' + tid)


class v_confession(View):
    def get(self, request):
        if not request.COOKIES.get("is_login"):
            return redirect('/account/login')
        uid = request.COOKIES.get('user_id')
        dbuser = UserInfo.objects.get(user_id=uid)
        con = confession.objects.filter()
        c_i = {}

        for i in con:
            c_i[i.id] = i.c_images_set.all()

        response = {
            'user': dbuser,
            'c_images': c_i,
            'confession': con
        }
        return render(request, 'function/confession.html', response)

    def post(self, request):
        if not request.COOKIES.get("is_login"):
            return redirect('/account/login')
        uid = request.COOKIES.get('user_id')

        c_title = request.POST.get('c_title')

        s_picture = request.FILES.getlist('c_picture')
        c_text = request.POST.get('c_text')
        c_kind = request.POST.get('c_kind')
        c_relation = request.POST.get('c_relation')
        con = confession.objects.create(c_title=c_title, c_uid=uid, c_text=c_text, c_kind=c_kind, c_relation=c_relation)
        for i in s_picture:
            c_picture_path = ''
            if i:
                # 保存文件
                c_picture_path = 'static/img/confession/' + uid + '_' + i.name
                f = open(os.path.join(c_picture_path), 'wb')
                for line in i.chunks():
                    f.write(line)
                f.close()
            c_images.objects.create(c_picture='/' + c_picture_path, confession=con)
        return redirect('/function/confession/')


def search_confession(request):
    if not request.COOKIES.get("is_login"):
        return redirect('/account/login')
    keys = request.POST.get('keys')
    if not keys:
        return redirect('/function/confession')
    uid = request.COOKIES.get('user_id')
    dbuser = UserInfo.objects.get(user_id=uid)
    con = confession.objects.filter(Q(c_title__contains=keys) | Q(c_text__contains=keys))
    c_i = {}

    for i in con:
        c_i[i.id] = i.c_images_set.all()
    print(1)
    response = {
        'user': dbuser,
        'c_images': c_i,
        'confession': con,
        'keys': keys
    }
    return render(request, 'function/confession.html', response)


class v_lost(View):
    def get(self, request):
        if not request.COOKIES.get("is_login"):
            return redirect('/account/login')
        uid = request.COOKIES.get('user_id')
        dbuser = UserInfo.objects.get(user_id=uid)
        lost1 = lost.objects.filter()
        l_i = {}
        print(lost1)
        for i in lost1:
            l_i[i.id] = i.l_images_set.all()

        response = {
            'user': dbuser,
            'l_images': l_i,
            'lost': lost1
        }
        return render(request, 'function/lost.html', response)

    def post(self, request):
        if not request.COOKIES.get("is_login"):
            return redirect('/account/login')
        uid = request.COOKIES.get('user_id')

        l_title = request.POST.get('l_title')
        l_picture = request.FILES.getlist('l_picture')
        l_text = request.POST.get('l_text')
        l_kind = request.POST.get('l_kind')
        l_relation = request.POST.get('l_relation')
        v_lost = lost.objects.create(l_title=l_title, l_uid=uid, l_text=l_text, l_kind=l_kind, l_relation=l_relation)
        for i in l_picture:
            l_picture_path = ''
            if i:
                # 保存文件
                l_picture_path = 'static/img/lost/' + uid + '_' + i.name
                f = open(os.path.join(l_picture_path), 'wb')
                for line in i.chunks():
                    f.write(line)
                f.close()
            l_images.objects.create(l_picture='/' + l_picture_path, lost=v_lost)
        return redirect('/function/lost/')


def search_lost(request):
    if not request.COOKIES.get("is_login"):
        return redirect('/account/login')
    keys = request.POST.get('keys')
    if not keys:
        return redirect('/function/lost')
    uid = request.COOKIES.get('user_id')
    dbuser = UserInfo.objects.get(user_id=uid)
    lost1 = lost.objects.filter(Q(l_title__contains=keys) | Q(l_text__contains=keys))
    l_i = {}
    for i in lost1:
        l_i[i.id] = i.l_images_set.all()
    response = {
        'user': dbuser,
        'l_images': l_i,
        'lost': lost1,
        'keys': keys
    }
    return render(request, 'function/lost.html', response)


class single_lost(View):
    def get(self, request, cid):
        if not request.COOKIES.get("is_login"):
            return redirect('/account/login')
        uid = request.COOKIES.get('user_id')
        dbuser = UserInfo.objects.get(user_id=uid)
        lost1 = lost.objects.get(id=cid)
        img = lost1.l_images_set.all()
        # 留言内容
        # 留言者，留言时间，留言内容
        replys = l_reply.objects.filter(l_tid=cid)
        reply_list = []

        for reply in replys:
            single_reply = {
                'r_uid': reply.l_uid,
                'r_time': reply.r_time,
                'r_content': reply.r_content,
                'r_id': reply.id,
                'r_photo': reply.r_photo,
            }
            reply_list.append(single_reply)

        response = {'lost': lost1, 'img': img, 'user': dbuser, 'reply_list': reply_list}

        return render(request, 'function/detail_lost.html', response)

    def post(self, request, cid):
        if not request.COOKIES.get("is_login"):
            return redirect('/account/login')
        # 进行回复
        print(77777777)
        r_content = request.POST.get('r_content')
        if not r_content:
            return redirect('/function/lostsingle/' + cid)
        uid = request.COOKIES.get('user_name')
        # 提交数据库
        obj = l_reply.objects.create(l_tid=cid, l_uid=uid, r_content=r_content)
        r_id = str(obj.id)
        r_photo = request.FILES.get('r_photo')
        r_photo_path = ''
        if r_photo:
            # 保存文件
            r_photo_path = 'static/img/lost/' + r_id + '_' + r_photo.name
            f = open(os.path.join(r_photo_path), 'wb')
            for line in r_photo.chunks():
                f.write(line)
            f.close()
        print(8888888888)
        # 吧图片路径存入数据库
        l_reply.objects.filter(id=r_id).update(r_photo='/' + r_photo_path)
        return redirect('/function/lostsingle/' + cid)


class single_confession(View):
    def get(self, request, cid):
        if not request.COOKIES.get("is_login"):
            return redirect('/account/login')
        uid = request.COOKIES.get('user_id')
        dbuser = UserInfo.objects.get(user_id=uid)
        con = confession.objects.get(id=cid)
        img = con.c_images_set.all()
        # 留言内容
        # 留言者，留言时间，留言内容
        replys = c_reply.objects.filter(c_tid=cid)
        reply_list = []

        for reply in replys:
            single_reply = {
                'r_uid': reply.c_uid,
                'r_time': reply.r_time,
                'r_content': reply.r_content,
                'r_id': reply.id,
                'r_photo': reply.r_photo,
            }
            reply_list.append(single_reply)

        response = {'confession': con, 'img': img, 'user': dbuser, 'reply_list': reply_list}

        return render(request, 'function/detail_confession.html', response)

    def post(self, request, cid):
        if not request.COOKIES.get("is_login"):
            return redirect('/account/login')
        # 进行回复
        r_content = request.POST.get('r_content')
        if not r_content:
            return redirect('/function/confessionsingle/' + cid)
        uid = request.COOKIES.get('user_name')
        # 提交数据库
        obj = c_reply.objects.create(c_tid=cid, c_uid=uid, r_content=r_content)
        r_id = str(obj.id)
        r_photo = request.FILES.get('r_photo')
        r_photo_path = ''
        if r_photo:
            # 保存文件
            r_photo_path = 'static/img/confession_reply/' + r_id + '_' + r_photo.name
            f = open(os.path.join(r_photo_path), 'wb')
            for line in r_photo.chunks():
                f.write(line)
            f.close()
        # 吧图片路径存入数据库
        c_reply.objects.filter(id=r_id).update(r_photo='/' + r_photo_path)
        return redirect('/function/confessionsingle/' + cid)


class cenery(View):

    def get(self, request, page_number):
        if not request.COOKIES.get("is_login"):
            return redirect('/account/login')
        uid = request.COOKIES.get('user_id')
        dbuser = UserInfo.objects.get(user_id=uid)
        all_senery = scenery.objects.filter(s_pass='1')
        paginator = Paginator(all_senery, 8)
        if paginator.num_pages >= int(page_number):
            page = paginator.page(int(page_number))
        else:
            page = paginator.page(paginator.num_pages)
        response = {
            'user': dbuser,
            'senery': page,
            'paginator': paginator,
            'page': page
        }
        return render(request, 'function/scenery.html', response)

    def post(self, request, page_number):
        if not request.COOKIES.get("is_login"):
            return redirect('/account/login')
        uid = request.COOKIES.get('user_name')
        s_text = request.POST.get('text')
        s_picture = request.FILES.get('s_picture')
        print(type(s_picture))
        s_picture_path = ''
        if s_picture:
            # 保存文件
            s_picture_path = 'static/img/scenery/' + uid + '_' + s_picture.name
            f = open(os.path.join(s_picture_path), 'wb')
            for line in s_picture.chunks():
                f.write(line)
            f.close()
        scenery.objects.create(s_uid=uid, s_text=s_text, s_picture='/' + s_picture_path)

        return redirect('/function/scenery/1/')
