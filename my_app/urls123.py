from django.urls import path

from .views123 import *

urlpatterns = [
    path('send_chat', send_chat, name='send_chat'),
    path('receive_chat', receive_chat, name='receive_chat'),
    path('chat_history', chat_history, name='chat_history'),
    path('create_team', create_team, name='create_team'),
    path('invite_member', invite_member, name='invite_member'),
    path('change_intro', change_intro, name='change_intro'),
    path('hot_achievement', hot_achievement, name='hot_achievement'),
    path('recommend_achievement', recommend_achievement, name='recommend_achievement'),
]