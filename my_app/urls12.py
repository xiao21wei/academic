from django.urls import path

from .views12 import *

urlpatterns = [
    path('send_register_email', send_register_email, name='send_register_email'),
    path('register', register, name='register'),
    path('login', login, name='login'),
    path('logout', logout, name='logout'),
    path('get_self_information', get_self_information, name='get_self_information'),
    path('get_intro_by_username', get_intro_by_username, name='get_intro_by_username'),
    path('set_scholar', set_scholar, name='set_scholar'),
    path('set_intro', set_intro, name='set_intro'),
    path('change_email', change_email, name='change_email'),
    path('change_password', change_password, name='change_password'),
]
