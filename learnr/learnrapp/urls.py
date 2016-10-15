from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'chat/', views.chat, name='chat'),
    url(r'send_message/', views.send_message, name='send_message'),
    url(r'register/', views.register, name='register'),
    url(r'login/', views.login, name='login'),
    url(r'get_messages/', views.get_messages, name='get_messages')
]