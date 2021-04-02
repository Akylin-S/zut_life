from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^forum-(?P<kid>\d+)-(?P<reply_limit>\d+)-(?P<time_limit>\d+)/(?P<page_number>\d+)/$', views.forum.as_view()),
    url(r'forumpub/', views.publish_forum),
    url(r'publish/', views.to_publish_forum),
    url(r'confession/', views.v_confession.as_view()),
    url(r'confessions/', views.search_confession),
    url(r'^confessionsingle/(?P<cid>\d+)/$', views.single_confession.as_view()),
    url(r'lost/', views.v_lost.as_view()),
    url(r'^single/(?P<tid>\d+)/', views.single),  # 单个帖子
    url(r'^scenery/(?P<page_number>\d+)/$', views.cenery.as_view())
]
