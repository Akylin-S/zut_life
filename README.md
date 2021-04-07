# 中工校园生活-web项目

这是一个基于django的web项目，用到mysql，jq，bootstrap，redis

## 项目部署
ubuntu+nginx+uwsgi+django
地址：http://123.60.11.43:8000/

## 实现的功能：
 * 注册登录功能
 * 验证码功能
 * 帖子发表功能
 * 帖子搜索筛选功能
 * 帖子回复功能
 * 帖子分类功能
 * 表白墙功能（失物招领）
 * 多图片，视频上传功能
 * 校园美景图片上传功能
 * 个人中心信息修改功能
 * 后台管理功能（删帖控评等）

## 正在改进的功能
 * 消息通知功能
 * 多级评论功能
 * 订阅功能和置顶功能
 * 通告发布功能
 * 界面美化和代码优化
 * ps目前想到这么多，以后会逐步改进

## 项目运行
 * setting 中<br>
    改成自己的数据库
```
  DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '127.0.0.1',  # 数据库主机
        'PORT': 3306,  # 数据库端口
        'USER': 'kylin',  # 数据库用户名
        'PASSWORD': '123456',  # 数据库用户密码
        'NAME': 'zut'  # 数据库名字
    }
} 
```

同理，cache也要改成自己的数据库

 *  安装依赖
```
  pip install -r requirements.txt
```

 * 数据迁移<br>
在根目录下运行

```
 python manage.py makemigrations
 python manage.py migrate
```

 ### 学习交流

点击进行 [学习交流](https://qm.qq.com/cgi-bin/qm/qr?k=fKyrqk9xxO9FRFyUEK5ayKHZcpXOga6W&authKey=hcMp8sTJyTk5KFu5T6WR1HNvO4ZWMNT4%2B7in8OqRufN3%2FuMMeLjaRLytvBmLksUY&noverify=0&group_code=821033535 "最好的markdown教程")

### 如果项目对你有帮助，可以给个星星吗！！！！！！！
