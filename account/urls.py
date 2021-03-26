from django.conf.urls import url

from . import views

urlpatterns = [
    url('^image_codes/(?P<image_code_id>[\w-]+)/$', views.ImageCodeView.as_view()),
    url('login/', views.login),
    url('sure1/', views.verifications.as_view()),
    url('register/', views.register),
    url('make_sure/', views.Verification_Register.as_view()),
    # url('success/', views.have_login)
]
