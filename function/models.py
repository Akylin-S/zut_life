from django.db import models


# 帖子表
class Topic(models.Model):
    t_uid = models.CharField(verbose_name='帖子所属用户id', max_length=16)
    t_kind = models.CharField(verbose_name='类别', max_length=32)
    create_time = models.DateField(verbose_name='创建时间', auto_now_add=True)
    t_photo = models.CharField(verbose_name='帖子图片', default='/static/img/forum.jpg',max_length=128, null=True)
    t_content = models.CharField(verbose_name='帖子正文', max_length=3000)
    t_title = models.CharField(verbose_name='帖子标题', max_length=64)
    t_introduce = models.CharField(verbose_name='帖子简介', max_length=256)

    class Meta:
        db_table = 'topic'  # 指明数据库表名
        verbose_name = '用户'  # 在admin站点中显示的名称
        verbose_name_plural = "所有用户"  # 显示的复数名称
        ordering = ('-id',)


# 回复表
class Reply(models.Model):
    r_tid = models.CharField(verbose_name='帖子id', max_length=16)
    r_uid = models.CharField(verbose_name='发表者id', max_length=16)
    r_photo = models.CharField(verbose_name='回复的图片', max_length=128, null=True)
    r_time = models.DateField(verbose_name='留言时间', auto_now_add=True)
    r_content = models.CharField(verbose_name='回复内容', max_length=3000)
    create_time = models.DateField(verbose_name='创建时间', auto_now_add=True)

    class Meta:
        ordering = ('-id',)


class scenery(models.Model):
    s_uid = models.CharField(verbose_name='上传者', max_length=16)
    s_picture = models.ImageField(upload_to="static/img/secenery",
                                  verbose_name='头像')
    s_text = models.CharField(verbose_name='图片简介', max_length=128, null=True, default='上传者很懒,没有简介')
    choices = (
        ('2', '待审核'),
        ('1', '通过'),
        ('0', '未通过'),
    )
    s_pass = models.CharField(verbose_name='审核', choices=choices, default='2', max_length=16)

    class Meta:
        db_table = 'scenery'  # 指明数据库表名
        ordering = ('-id',)


class confession(models.Model):
    c_uid = models.CharField(verbose_name='发布者', max_length=16)
    c_title = models.CharField(verbose_name='标题', max_length=30)
    c_text = models.CharField(verbose_name='回复内容', max_length=3000)
    c_relation = models.CharField(verbose_name='联系方式', max_length=150)
    create_time = models.DateField(verbose_name='发布时间', auto_now_add=True)
    choices = (
        ('1', '卖室友'),
        ('0', '表白'),
    )
    c_kind = models.CharField(verbose_name='类型', choices=choices, max_length=150)

    class Meta:
        db_table = 'confession'  # 指明数据库表名
        ordering = ('-id',)


class c_images(models.Model):
    c_picture = models.ImageField(upload_to='static/img/confession', verbose_name='图片')
    confession = models.ForeignKey('confession', on_delete=models.CASCADE)

    class Meta:
        db_table = 'c_images'
        ordering = ('-id',)


class c_reply(models.Model):
    c_tid = models.CharField(verbose_name='表白墙id', max_length=16)
    c_uid = models.CharField(verbose_name='发表者id', max_length=16)
    r_photo = models.ImageField(upload_to='static/imag/confession_reply/',verbose_name='回复的图片', max_length=128, null=True)
    r_time = models.DateField(verbose_name='留言时间', auto_now_add=True)
    r_content = models.CharField(verbose_name='回复内容', max_length=3000)

    class Meta:
        db_table = 'confession_reply'
        ordering = ('-id',)


class lost(models.Model):
    l_uid = models.CharField(verbose_name='发布者', max_length=16)
    l_title = models.CharField(verbose_name='标题', max_length=30)
    l_text = models.CharField(verbose_name='回复内容', max_length=3000)
    l_relation = models.CharField(verbose_name='联系方式', max_length=150)
    create_time = models.DateField(verbose_name='发布时间', auto_now_add=True)
    choices = (
        ('1', '物寻人'),
        ('0', '人寻物'),
    )
    l_kind = models.CharField(verbose_name='类型', choices=choices, max_length=150)

    class Meta:
        db_table = 'lost'  # 指明数据库表名
        ordering = ('-id',)


class l_images(models.Model):
    l_picture = models.ImageField(upload_to='static/img/confession', verbose_name='图片')
    lost = models.ForeignKey('lost', on_delete=models.CASCADE)

    class Meta:
        db_table = 'l_images'
        ordering = ('-id',)


class l_reply(models.Model):
    l_tid = models.CharField(verbose_name='失物招领id', max_length=16)
    l_uid = models.CharField(verbose_name='发表者id', max_length=16)
    r_photo = models.ImageField(upload_to='static/imag/lost_reply/',verbose_name='回复的图片', max_length=128, null=True)
    r_time = models.DateField(verbose_name='留言时间', auto_now_add=True)
    r_content = models.CharField(verbose_name='回复内容', max_length=3000)

    class Meta:
        db_table = 'l_reply'
        ordering = ('-id',)
