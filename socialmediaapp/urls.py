from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_list, {'username': None}, name='home'),
    path('chat/', views.chat_list, {'username': None}, name='chat_list'),
    path('chat/<str:username>/', views.chat_view, name='chat'),
    path('send-message/', views.send_message, name='send_message'),
    path('chat/<str:username>/get-messages/', views.get_messages, name='get_messages'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
]