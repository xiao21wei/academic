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
    path('get_achievements_by_time', get_achievements_by_time, name='get_achievements_by_time'),
    # path('send_verification_code', send_verification_code, name='send_verification_code'),
    path('report_achievement', report_achievement, name='report_achievement'),
    path('check_report', check_report, name='check_report'),
    path('get_report', get_report, name='get_report'),
    path('get_report_list', get_report_list, name='get_report_list'),
    path('get_unchecked_report_list', get_unchecked_report_list, name='get_unchecked_report_list'),
    path('get_checked_report_list', get_checked_report_list, name='get_checked_report_list'),
    path('get_report_list_by_achievement', get_report_list_by_achievement, name='get_report_list_by_achievement'),
    path('get_report_list_by_user', get_report_list_by_user, name='get_report_list_by_user'),
    path('get_report_list_by_admin', get_report_list_by_admin, name='get_report_list_by_admin'),
    path('like_achievement', like_achievement, name='like_achievement'),
    path('cancel_like_achievement', cancel_like_achievement, name='cancel_like_achievement'),
    path('get_like_list_by_achievement', get_like_list_by_achievement, name='get_like_list_by_achievement'),
    path('get_like_list_by_user', get_like_list_by_user, name='get_like_list_by_user'),
    path('get_like_count_by_achievement', get_like_count_by_achievement, name='get_like_count_by_achievement'),
    path('comment_achievement', comment_achievement, name='comment_achievement'),
    path('delete_comment', delete_comment, name='delete_comment'),
    path('get_comment_list_by_achievement', get_comment_list_by_achievement, name='get_comment_list_by_achievement'),
    path('get_comment_list_by_user', get_comment_list_by_user, name='get_comment_list_by_user'),
    path('get_comment_count_by_achievement', get_comment_count_by_achievement, name='get_comment_count_by_achievement'),
    path('get_comment_count_by_user', get_comment_count_by_user, name='get_comment_count_by_user'),
    path('collect_achievement', collect_achievement, name='collect_achievement'),
    path('cancel_collect_achievement', cancel_collect_achievement, name='cancel_collect_achievement'),
    path('get_collect_count_by_achievement', get_collect_count_by_achievement, name='get_collect_count_by_achievement'),
    path('get_collect_count_by_user', get_collect_count_by_user, name='get_collect_count_by_user'),
    path('get_collect_list_by_achievement', get_collect_list_by_achievement, name='get_collect_list_by_achievement'),
    path('get_collect_list_by_user', get_collect_list_by_user, name='get_collect_list_by_user'),
    path('index', index, name='index'),
    path('search', search, name='search'),
    path('check_achievement', check_achievement, name='check_achievement'),
    path('get_count', get_count, name='get_count'),
]
