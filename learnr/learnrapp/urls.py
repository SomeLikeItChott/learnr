from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'chat/', views.chat, name='chat'),
    url(r'send_message/', views.send_message, name='send_message')
]