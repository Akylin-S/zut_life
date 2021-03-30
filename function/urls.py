from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^forum-(?P<kid>\d+)-(?P<reply_limit>\d+)-(?P<time_limit>\d+)/(?P<page_number>\d+)/$', views.forum.as_view()),
    url('forumpub/', views.publish_forum),
    url('publish/', views.to_publish_forum),
    url('confession/',views.confession),
    url('lost/', views.lost),
    url(r'^single/(?P<tid>\d+)/', views.single),  # 单个帖子
]
