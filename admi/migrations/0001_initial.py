# Generated by Django 3.1.7 on 2021-03-30 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BackUser',
            fields=[
                ('back_id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('back_user', models.CharField(max_length=20, verbose_name='用户名')),
                ('back_password', models.CharField(max_length=20, verbose_name='密码')),
            ],
        ),
        migrations.CreateModel(
            name='DayNumber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.DateField(auto_now=True, verbose_name='日期')),
                ('visit_count', models.IntegerField(default=0, verbose_name='网站访问次数')),
            ],
            options={
                'verbose_name': '网站日访问量统计',
                'verbose_name_plural': '网站日访问量统计',
            },
        ),
    ]
