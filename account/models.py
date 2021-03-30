from django.db import models


# Create your models here.
class UserInfo(models.Model):
    user_id = models.AutoField(primary_key=True, verbose_name='ID')
    user = models.CharField(max_length=20, verbose_name='用户名')
    password = models.CharField(max_length=16, verbose_name='密码')
    phone = models.BigIntegerField(null=True, verbose_name='手机号')
    email = models.CharField(max_length=30, null=True, verbose_name='邮箱')
    user_img = models.ImageField(upload_to="static/img/user_img", default='static/account/picture.jpg',
                                 verbose_name='头像')
    choices = (
        ('male', '男性'),
        ('female', '女性'),
    )
    gender = models.CharField(max_length=6, choices=choices, default='male')

    class Meta:
        db_table = 'userinfo'  # 指明数据库表名
        verbose_name = '用户'  # 在admin站点中显示的名称
        verbose_name_plural = "所有用户"  # 显示的复数名称

    def __str__(self):
        """定义每个数据对象的显示信息"""
        return self.user

