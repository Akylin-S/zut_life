from django.conf.urls import url

from . import views

urlpatterns = [
    url('success', views.Confession.as_view()),
]
