from django.urls import path

from .views import *

urlpatterns = [
    path('publish_achievement', publish_achievement, name='publish_achievement'),
    path('get_achievement', get_achievement, name='get_achievement'),
    path('get_achievements', get_achievements, name='get_achievements'),
    path('update_achievement', update_achievement, name='update_achievement'),
    path('delete_achievement', delete_achievement, name='delete_achievement'),
    path('get_achievements_by_type', get_achievements_by_type, name='get_achievements_by_type'),
    path('get_achievements_by_area', get_achievements_by_area, name='get_achievements_by_area'),
    path('get_achievements_by_name', get_achievements_by_name, name='get_achievements_by_name'),
    path('get_achievements_by_author', get_achievements_by_author, name='get_achievements_by_author'),
    path('get_achievements_by_time', get_achievements_by_time, name='get_achievements_by_time')
]
