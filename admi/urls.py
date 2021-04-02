from django.conf.urls import url
from admi import views

urlpatterns = [
    # url(r'backstageManage/', views.backstage_manage.as_view()),
    # url(r'logout/',views.logout),
    # url(r'usermanage/(?P<page>[0-9]+)/',views.usermanage),
    # url(r'postmanage/(?P<page>[0-9]+)/',views.postmanage),
    #
    # url(r'post/past/(?P<postid>[0-9]+)/',views.past),
    # url(r'post/notpast/(?P<postid>[0-9]+)/',views.notPast),
    #
    # url(r'unreviewed/',views.unreviewed_manage),
    # url(r'past/',views.past_manage),
    # url(r'fail/',views.notpast_manage),
    #
    # url(r'delete/(?P<postid>[0-9]+)/',views.delete_post),
    #
    # url(r'',views.index)
    url(r'login/', views.login.as_view()),
    url(r'home/', views.home.as_view()),
    url(r'user/', views.user_admin.as_view()),
    url(r'forum/', views.forum_admin.as_view()),
    url(r'scenery/', views.admin_scenery.as_view()),
    url(r'logout/', views.logout),
]
