from django.db import models

# Create your models here


class BackUser(models.Model):
    back_id = models.AutoField( primary_key=True, verbose_name='ID')
    back_user = models.CharField(max_length=20, verbose_name='用户名')
    back_password = models.CharField(max_length=20, verbose_name='密码')


class DayNumber(models.Model):
    day = models.DateField(verbose_name='日期', auto_now=True)
    visit_count = models.IntegerField(verbose_name='网站访问次数', default=0)  # 网站访问总次数

    class Meta:
        verbose_name = '网站日访问量统计'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.day)
