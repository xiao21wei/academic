import os
import random
import time
import uuid

from django import forms
from django.db import transaction
from django.shortcuts import render

from academic.settings import MEDIA_ROOT
from django.http import JsonResponse, FileResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from academic.tools import check_session
from datetime import datetime
import difflib

from my_app.models import *


# Create your views here.

# 发布学术成果
@csrf_exempt  # 跨域设置
def publish_achievement(request):
    if request.method == 'POST':
        id = check_session(request)
        if id == 0:
            return JsonResponse({'error': '-1', 'msg': '请先登录'})
        name = request.POST.get('name')
        # 获取author_id列表信息，并用'_'拼接成字符串
        author_id = '_'.join(request.POST.getlist('author_id'))
        author_id = '_'+author_id+'_'
        intro = request.POST.get('intro')
        url = request.POST.get('url')
        type = request.POST.get('type')
        # 获取area列表信息，并用'_'拼接成字符串
        area = '_'.join(request.POST.getlist('area'))
        area = '_'+area+'_'
        achievement = Achievement(name=name, author_id=author_id, intro=intro, url=url, type=type, area=area)
        achievement.save()  # 保存到数据库
        return JsonResponse({'error': '0', 'msg': '学术成果发布成功'})
    else:
        return JsonResponse({'error': '1001', 'msg': '请求方式错误'})


# 获取学术成果详情
@csrf_exempt  # 跨域设置
def get_achievement(request):
    if request.method == 'POST':
        id = check_session(request)
        if id == 0:
            return JsonResponse({'error': '-1', 'msg': '请先登录'})
        achievement_id = request.POST.get('achievement_id')
        achievement = Achievement.objects.get(achievement_id=achievement_id)
        if achievement:
            return JsonResponse({'error': '0', 'msg': '获取学术成果成功', 'data': {
                'achievement_id': achievement.achievement_id,
                'name': achievement.name,
                # 用'_'分割字符串，去除空，返回列表
                'author_id': list(filter(None, achievement.author_id.split('_'))),
                'intro': achievement.intro,
                'url': achievement.url,
                'type': achievement.type,
                # 用'_'分割字符串，去除空，返回列表
                'area': list(filter(None, achievement.area.split('_'))),
                'create_time': achievement.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            }})
        else:
            return JsonResponse({'error': '1002', 'msg': '学术成果不存在'})
    else:
        return JsonResponse({'error': '1001', 'msg': '请求方式错误'})


# 获取学术成果列表
@csrf_exempt  # 跨域设置
def get_achievements(request):
    if request.method == 'POST':
        id = check_session(request)
        if id == 0:
            return JsonResponse({'error': '-1', 'msg': '请先登录'})
        achievements = Achievement.objects.all()
        if achievements:
            return JsonResponse({'error': '0', 'msg': '获取学术成果成功', 'data': [  # 结果按照create_time降序排列
                {
                    'achievement_id': achievement.achievement_id,
                    'name': achievement.name,
                    # 用'_'分割字符串，去除空，返回列表
                    'author_id': list(filter(None, achievement.author_id.split('_'))),
                    'intro': achievement.intro,
                    'url': achievement.url,
                    'type': achievement.type,
                    # 用'_'分割字符串，去除空，返回列表
                    'area': list(filter(None, achievement.area.split('_'))),
                    'create_time': achievement.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                } for achievement in achievements.order_by('-create_time')
            ]})
        else:
            return JsonResponse({'error': '1002', 'msg': '学术成果不存在'})
    else:
        return JsonResponse({'error': '1001', 'msg': '请求方式错误'})


# 更新学术成果
@csrf_exempt  # 跨域设置
def update_achievement(request):
    if request.method == 'POST':
        id = check_session(request)
        if id == 0:
            return JsonResponse({'error': '-1', 'msg': '请先登录'})
        achievement_id = request.POST.get('achievement_id')
        achievement = Achievement.objects.get(achievement_id=achievement_id)
        if achievement:
            # 获取author_id的第一个值，即为作者id
            author_id = achievement.author_id.split('_')[0]
            if author_id == id:
                name = request.POST.get('name')
                intro = request.POST.get('intro')
                url = request.POST.get('url')
                type = request.POST.get('type')
                author_id = '_'.join(request.POST.getlist('author_id'))
                author_id = '_'+author_id+'_'
                area = '_'.join(request.POST.getlist('area'))
                area = '_'+area+'_'
                achievement.area = area
                achievement.name = name
                achievement.intro = intro
                achievement.url = url
                achievement.type = type
                achievement.author_id = author_id
                achievement.save()
                return JsonResponse({'error': '0', 'msg': '学术成果更新成功'})
            else:
                return JsonResponse({'error': '1003', 'msg': '无权限更新该学术成果'})
        else:
            return JsonResponse({'error': '1002', 'msg': '学术成果不存在'})
    else:
        return JsonResponse({'error': '1001', 'msg': '请求方式错误'})


# 删除学术成果
@csrf_exempt  # 跨域设置
def delete_achievement(request):
    if request.method == 'POST':
        id = check_session(request)
        if id == 0:
            return JsonResponse({'error': '-1', 'msg': '请先登录'})
        achievement_id = request.POST.get('achievement_id')
        user_id = request.POST.get('user_id')
        achievement = Achievement.objects.get(achievement_id=achievement_id)
        if achievement:
            # 获取author_id的第一个值，即为作者id
            author_id = achievement.author_id.split('_')[1]
            if author_id == user_id:
                achievement.delete()
                return JsonResponse({'error': '0', 'msg': '学术成果删除成功'})
            else:
                return JsonResponse({'error': '1003', 'msg': '无权限删除该学术成果'})
        else:
            return JsonResponse({'error': '1002', 'msg': '学术成果不存在'})
    else:
        return JsonResponse({'error': '1001', 'msg': '请求方式错误'})


# 根据领域获取学术成果
@csrf_exempt  # 跨域设置
def get_achievements_by_area(request):
    if request.method == 'POST':
        id = check_session(request)
        if id == 0:
            return JsonResponse({'error': '-1', 'msg': '请先登录'})
        area = request.POST.get('area')
        achievements = Achievement.objects.filter(area__contains='_'+area+'_')
        if achievements:
            return JsonResponse({'error': '0', 'msg': '获取学术成果成功', 'data': [
                {
                    'achievement_id': achievement.achievement_id,
                    'name': achievement.name,
                    # 用'_'分割字符串，去除空，返回列表
                    'author_id': list(filter(None, achievement.author_id.split('_'))),
                    'intro': achievement.intro,
                    'url': achievement.url,
                    'type': achievement.type,
                    # 用'_'分割字符串，去除空，返回列表
                    'area': list(filter(None, achievement.area.split('_'))),
                    'create_time': achievement.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                } for achievement in achievements.order_by('-create_time')
            ]})
        else:
            return JsonResponse({'error': '1002', 'msg': '学术成果不存在'})
    else:
        return JsonResponse({'error': '1001', 'msg': '请求方式错误'})


# 通过类型获取学术成果
@csrf_exempt  # 跨域设置
def get_achievements_by_type(request):
    if request.method == 'POST':
        id = check_session(request)
        if id == 0:
            return JsonResponse({'error': '-1', 'msg': '请先登录'})
        type = request.POST.get('type')
        achievements = Achievement.objects.filter(type=type)
        if achievements:
            return JsonResponse({'error': '0', 'msg': '获取学术成果成功', 'data': [
                {
                    'achievement_id': achievement.achievement_id,
                    'name': achievement.name,
                    # 用'_'分割字符串，去除空，返回列表
                    'author_id': list(filter(None, achievement.author_id.split('_'))),
                    'intro': achievement.intro,
                    'url': achievement.url,
                    'type': achievement.type,
                    # 用'_'分割字符串，去除空，返回列表
                    'area': list(filter(None, achievement.area.split('_'))),
                    'create_time': achievement.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                } for achievement in achievements.order_by('-create_time')
            ]})
        else:
            return JsonResponse({'error': '1002', 'msg': '学术成果不存在'})
    else:
        return JsonResponse({'error': '1001', 'msg': '请求方式错误'})


# 根据学术成果名字获取学术成果
@csrf_exempt  # 跨域设置
def get_achievements_by_name(request):
    if request.method == 'POST':
        id = check_session(request)
        if id == 0:
            return JsonResponse({'error': '-1', 'msg': '请先登录'})
        name = request.POST.get('name')
        achievements = Achievement.objects.filter(name__contains=name)
        if achievements:
            return JsonResponse({'error': '0', 'msg': '获取学术成果成功', 'data': [
                {
                    'achievement_id': achievement.achievement_id,
                    'name': achievement.name,
                    # 用'_'分割字符串，去除空，返回列表
                    'author_id': list(filter(None, achievement.author_id.split('_'))),
                    'intro': achievement.intro,
                    'url': achievement.url,
                    'type': achievement.type,
                    # 用'_'分割字符串，去除空，返回列表
                    'area': list(filter(None, achievement.area.split('_'))),
                    'create_time': achievement.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                } for achievement in achievements.order_by('-create_time')
            ]})
        else:
            return JsonResponse({'error': '1002', 'msg': '学术成果不存在'})
    else:
        return JsonResponse({'error': '1001', 'msg': '请求方式错误'})


# 通过作者id获取学术成果
@csrf_exempt  # 跨域设置
def get_achievements_by_author(request):
    if request.method == 'POST':
        id = check_session(request)
        if id == 0:
            return JsonResponse({'error': '-1', 'msg': '请先登录'})
        author = request.POST.get('author')
        achievements = Achievement.objects.filter(author_id__contains='_'+author+'_')
        if achievements:
            return JsonResponse({'error': '0', 'msg': '获取学术成果成功', 'data': [
                {
                    'achievement_id': achievement.achievement_id,
                    'name': achievement.name,
                    # 用'_'分割字符串，去除空，返回列表
                    'author_id': list(filter(None, achievement.author_id.split('_'))),
                    'intro': achievement.intro,
                    'url': achievement.url,
                    'type': achievement.type,
                    # 用'_'分割字符串，去除空，返回列表
                    'area': list(filter(None, achievement.area.split('_'))),
                    'create_time': achievement.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                } for achievement in achievements.order_by('-create_time')
            ]})
        else:
            return JsonResponse({'error': '1002', 'msg': '学术成果不存在'})
    else:
        return JsonResponse({'error': '1001', 'msg': '请求方式错误'})


# 通过时间获取学术成果
@csrf_exempt  # 跨域设置
def get_achievements_by_time(request):
    if request.method == 'POST':
        id = check_session(request)
        if id == 0:
            return JsonResponse({'error': '-1', 'msg': '请先登录'})
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        achievements = Achievement.objects.filter(create_time__range=(start_time, end_time))
        if achievements:
            return JsonResponse({'error': '0', 'msg': '获取学术成果成功', 'data': [
                {
                    'achievement_id': achievement.achievement_id,
                    'name': achievement.name,
                    # 用'_'分割字符串，去除空，返回列表
                    'author_id': list(filter(None, achievement.author_id.split('_'))),
                    'intro': achievement.intro,
                    'url': achievement.url,
                    'type': achievement.type,
                    # 用'_'分割字符串，去除空，返回列表
                    'area': list(filter(None, achievement.area.split('_'))),
                    'create_time': achievement.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                } for achievement in achievements.order_by('-create_time')
            ]})
        else:
            return JsonResponse({'error': '1002', 'msg': '学术成果不存在'})
    else:
        return JsonResponse({'error': '1001', 'msg': '请求方式错误'})


# 发送验证码
# @csrf_exempt  # 跨域设置
# def send_verification_code(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         send_type = request.POST.get('send_type')
#         flag = send_sms_code(email, send_type)
#         if flag:
#             return JsonResponse({'error': '0', 'msg': '发送验证码成功'})
#         else:
#             return JsonResponse({'error': '1002', 'msg': '发送验证码失败'})
#     else:
#         return JsonResponse({'error': '1001', 'msg': '请求方式错误'})


# 举报学术成果
@csrf_exempt  # 跨域设置
def report_achievement(request):
    if request.method == 'POST':
        id = check_session(request)
        if id == 0:
            return JsonResponse({'error': '-1', 'msg': '请先登录'})
        user_id = request.POST.get('user_id')
        achievement_id = request.POST.get('achievement_id')
        content = request.POST.get('content')
        report = Report(send=user_id, achievement_id=achievement_id, content=content)
        report.save()
        return JsonResponse({'error': '0', 'msg': '举报提交成功'})
    else:
        return JsonResponse({'error': '1001', 'msg': '请求方式错误'})


# 审核举报
@csrf_exempt  # 跨域设置
def check_report(request):
    if request.method == 'POST':
        id = check_session(request)
        if id == 0:
            return JsonResponse({'error': '-1', 'msg': '请先登录'})
        report_id = request.POST.get('report_id')
        admin_id = request.POST.get('admin_id')
        result = request.POST.get('result')
        report = Report.objects.get(report_id=report_id)
        # 如果report.result为空，说明该举报未被审核
        if report.result == '':
            report.result = result
            report.admin_id = admin_id
            report.save()
            return JsonResponse({'error': '0', 'msg': '审核成功'})
        else:
            return JsonResponse({'error': '1002', 'msg': '该举报已被审核'})
    else:
        return JsonResponse({'error': '1001', 'msg': '请求方式错误'})


# 获取举报信息
@csrf_exempt  # 跨域设置
def get_report(request):
    if request.method == 'POST':
        id = check_session(request)
        if id == 0:
            return JsonResponse({'error': '-1', 'msg': '请先登录'})
        report_id = request.POST.get('report_id')
        report = Report.objects.get(report_id=report_id)
        if report:
            return JsonResponse({'error': '0', 'msg': '获取举报信息成功', 'data': {
                'report_id': report.report_id,
                'send': report.send,
                'achievement_id': report.achievement_id,
                'content': report.content,
                'result': report.result,
                'admin_id': report.admin_id,
                'create_time': report.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            }})
        else:
            return JsonResponse({'error': '1002', 'msg': '举报信息不存在'})
    else:
        return JsonResponse({'error': '1001', 'msg': '请求方式错误'})


# 获取举报列表
@csrf_exempt  # 跨域设置
def get_report_list(request):
    if request.method == 'POST':
        id = check_session(request)
        if id == 0:
            return JsonResponse({'error': '-1', 'msg': '请先登录'})
        report_list = Report.objects.all()
        if report_list:
            return JsonResponse({'error': '0', 'msg': '获取举报列表成功', 'data': [
                {
                    'report_id': report.report_id,
                    'send': report.send,
                    'achievement_id': report.achievement_id,
                    'content': report.content,
                    'result': report.result,
                    'admin_id': report.admin_id,
                    'create_time': report.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                } for report in report_list.order_by('-create_time')
            ]})
        else:
            return JsonResponse({'error': '1002', 'msg': '举报列表为空'})
    else:
        return JsonResponse({'error': '1001', 'msg': '请求方式错误'})


# 获取未审核列表
@csrf_exempt  # 跨域设置
def get_unchecked_report_list(request):
    if request.method == 'POST':
        id = check_session(request)
        if id == 0:
            return JsonResponse({'error': '-1', 'msg': '请先登录'})
        report_list = Report.objects.filter(result='')
        if report_list:
            return JsonResponse({'error': '0', 'msg': '获取举报列表成功', 'data': [
                {
                    'report_id': report.report_id,
                    'send': report.send,
                    'achievement_id': report.achievement_id,
                    'content': report.content,
                    'result': report.result,
                    'admin_id': report.admin_id,
                    'create_time': report.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                } for report in report_list.order_by('-create_time')
            ]})
        else:
            return JsonResponse({'error': '1002', 'msg': '举报列表为空'})
    else:
        return JsonResponse({'error': '1001', 'msg': '请求方式错误'})


# 获取已审核列表
@csrf_exempt  # 跨域设置
def get_checked_report_list(request):
    if request.method == 'POST':
        id = check_session(request)
        if id == 0:
            return JsonResponse({'error': '-1', 'msg': '请先登录'})
        report_list = Report.objects.exclude(result='')
        if report_list:
            return JsonResponse({'error': '0', 'msg': '获取举报列表成功', 'data': [
                {
                    'report_id': report.report_id,
                    'send': report.send,
                    'achievement_id': report.achievement_id,
                    'content': report.content,
                    'result': report.result,
                    'admin_id': report.admin_id,
                    'create_time': report.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                } for report in report_list.order_by('-create_time')
            ]})
        else:
            return JsonResponse({'error': '1002', 'msg': '举报列表为空'})
    else:
        return JsonResponse({'error': '1001', 'msg': '请求方式错误'})


# 获取某成果的举报列表
@csrf_exempt  # 跨域设置
def get_report_list_by_achievement(request):
    if request.method == 'POST':
        id = check_session(request)
        if id == 0:
            return JsonResponse({'error': '-1', 'msg': '请先登录'})
        achievement_id = request.POST.get('achievement_id')
        report_list = Report.objects.filter(achievement_id=achievement_id)
        if report_list:
            return JsonResponse({'error': '0', 'msg': '获取举报列表成功', 'data': [
                {
                    'report_id': report.report_id,
                    'send': report.send,
                    'achievement_id': report.achievement_id,
                    'content': report.content,
                    'result': report.result,
                    'admin_id': report.admin_id,
                    'create_time': report.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                } for report in report_list.order_by('-create_time')
            ]})
        else:
            return JsonResponse({'error': '1002', 'msg': '举报列表为空'})
    else:
        return JsonResponse({'error': '1001', 'msg': '请求方式错误'})


# 获取某用户的举报列表
@csrf_exempt  # 跨域设置
def get_report_list_by_user(request):
    if request.method == 'POST':
        id = check_session(request)
        if id == 0:
            return JsonResponse({'error': '-1', 'msg': '请先登录'})
        user_id = request.POST.get('user_id')
        report_list = Report.objects.filter(send=user_id)
        if report_list:
            return JsonResponse({'error': '0', 'msg': '获取举报列表成功', 'data': [
                {
                    'report_id': report.report_id,
                    'send': report.send,
                    'achievement_id': report.achievement_id,
                    'content': report.content,
                    'result': report.result,
                    'admin_id': report.admin_id,
                    'create_time': report.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                } for report in report_list.order_by('-create_time')
            ]})
        else:
            return JsonResponse({'error': '1002', 'msg': '举报列表为空'})
    else:
        return JsonResponse({'error': '1001', 'msg': '请求方式错误'})


# 获取某管理员审核的举报列表
@csrf_exempt  # 跨域设置
def get_report_list_by_admin(request):
    if request.method == 'POST':
        id = check_session(request)
        if id == 0:
            return JsonResponse({'error': '-1', 'msg': '请先登录'})
        admin_id = request.POST.get('admin_id')
        report_list = Report.objects.filter(admin=admin_id)
        if report_list:
            return JsonResponse({'error': '0', 'msg': '获取举报列表成功', 'data': [
                {
                    'report_id': report.report_id,
                    'send': report.send,
                    'achievement_id': report.achievement_id,
                    'content': report.content,
                    'result': report.result,
                    'admin_id': report.admin_id,
                    'create_time': report.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                } for report in report_list.order_by('-create_time')
            ]})
        else:
            return JsonResponse({'error': '1002', 'msg': '举报列表为空'})
    else:
        return JsonResponse({'error': '1001', 'msg': '请求方式错误'})


# 点赞学术成果
@csrf_exempt  # 跨域设置
def like_achievement(request):
    if request.method == 'POST':
        id = check_session(request)
        if id == 0:
            return JsonResponse({'error': '-1', 'msg': '请先登录'})
        achievement_id = request.POST.get('achievement_id')
        user_id = request.POST.get('user_id')
        like = Like.objects.filter(achievement_id=achievement_id, user_id=user_id)
        if like:
            return JsonResponse({'error': '1003', 'msg': '已点赞'})
        else:
            like = Like.objects.create(achievement_id=achievement_id, user_id=user_id)
            if like:
                return JsonResponse({'error': '0', 'msg': '点赞成功'})
            else:
                return JsonResponse({'error': '1002', 'msg': '点赞失败'})
    else:
        return JsonResponse({'error': '1001', 'msg': '请求方式错误'})


# 取消点赞学术成果
@csrf_exempt  # 跨域设置
def cancel_like_achievement(request):
    if request.method == 'POST':
        id = check_session(request)
        if id == 0:
            return JsonResponse({'error': '-1', 'msg': '请先登录'})
        achievement_id = request.POST.get('achievement_id')
        user_id = request.POST.get('user_id')
        like = Like.objects.filter(achievement_id=achievement_id, user_id=user_id)
        if like:
            like.delete()
            return JsonResponse({'error': '0', 'msg': '取消点赞成功'})
        else:
            return JsonResponse({'error': '1003', 'msg': '未点赞'})
    else:
        return JsonResponse({'error': '1001', 'msg': '请求方式错误'})


# 获取某学术成果的点赞列表
@csrf_exempt  # 跨域设置
def get_like_list_by_achievement(request):
    if request.method == 'POST':
        id = check_session(request)
        if id == 0:
            return JsonResponse({'error': '-1', 'msg': '请先登录'})
        achievement_id = request.POST.get('achievement_id')
        like_list = Like.objects.filter(achievement_id=achievement_id)
        if like_list:
            return JsonResponse({'error': '0', 'msg': '获取点赞列表成功', 'data': [
                {
                    'user_id': like.user_id,
                } for like in like_list
            ]})
        else:
            return JsonResponse({'error': '1002', 'msg': '点赞列表为空'})
    else:
        return JsonResponse({'error': '1001', 'msg': '请求方式错误'})


# 获取某用户点赞的学术成果列表
@csrf_exempt  # 跨域设置
def get_like_list_by_user(request):
    if request.method == 'POST':
        id = check_session(request)
        if id == 0:
            return JsonResponse({'error': '-1', 'msg': '请先登录'})
        user_id = request.POST.get('user_id')
        like_list = Like.objects.filter(user_id=user_id)
        if like_list:
            return JsonResponse({'error': '0', 'msg': '获取点赞列表成功', 'data': [
                {
                    'achievement_id': like.achievement_id,
                } for like in like_list
            ]})
        else:
            return JsonResponse({'error': '1002', 'msg': '点赞列表为空'})
    else:
        return JsonResponse({'error': '1001', 'msg': '请求方式错误'})


# 获取某学术成果的点赞数
@csrf_exempt  # 跨域设置
def get_like_count_by_achievement(request):
    if request.method == 'POST':
        id = check_session(request)
        if id == 0:
            return JsonResponse({'error': '-1', 'msg': '请先登录'})
        achievement_id = request.POST.get('achievement_id')
        like_count = Like.objects.filter(achievement_id=achievement_id).count()
        return JsonResponse({'error': '0', 'msg': '获取点赞数成功', 'data': like_count})
    else:
        return JsonResponse({'error': '1001', 'msg': '请求方式错误'})


# 评论学术成果
@csrf_exempt  # 跨域设置
def comment_achievement(request):
    if request.method == 'POST':
        id = check_session(request)
        if id == 0:
            return JsonResponse({'error': '-1', 'msg': '请先登录'})
        achievement_id = request.POST.get('achievement_id')
        user_id = request.POST.get('user_id')
        content = request.POST.get('content')
        comment = Comment.objects.create(achievement_id=achievement_id, user_id=user_id, content=content)
        if comment:
            return JsonResponse({'error': '0', 'msg': '评论成功'})
        else:
            return JsonResponse({'error': '1002', 'msg': '评论失败'})
    else:
        return JsonResponse({'error': '1001', 'msg': '请求方式错误'})


# 删除评论
@csrf_exempt  # 跨域设置
def delete_comment(request):
    if request.method == 'POST':
        id = check_session(request)
        if id == 0:
            return JsonResponse({'error': '-1', 'msg': '请先登录'})
        comment_id = request.POST.get('comment_id')
        user_id = request.POST.get('user_id')
        comment = Comment.objects.filter(id=comment_id, user_id=user_id)
        if comment:
            comment.delete()
            return JsonResponse({'error': '0', 'msg': '删除成功'})
        else:
            return JsonResponse({'error': '1003', 'msg': '评论不存在'})
    else:
        return JsonResponse({'error': '1001', 'msg': '请求方式错误'})


# 获取某学术成果的评论列表
@csrf_exempt  # 跨域设置
def get_comment_list_by_achievement(request):
    if request.method == 'POST':
        id = check_session(request)
        if id == 0:
            return JsonResponse({'error': '-1', 'msg': '请先登录'})
        achievement_id = request.POST.get('achievement_id')
        comment_list = Comment.objects.filter(achievement_id=achievement_id)
        if comment_list:
            return JsonResponse({'error': '0', 'msg': '获取评论列表成功', 'data': [
                {
                    'user_id': comment.user_id,
                    'content': comment.content,
                    'create_time': comment.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                } for comment in comment_list
            ]})
        else:
            return JsonResponse({'error': '1002', 'msg': '评论列表为空'})
    else:
        return JsonResponse({'error': '1001', 'msg': '请求方式错误'})


# 获取某用户评论的学术成果列表
@csrf_exempt  # 跨域设置
def get_comment_list_by_user(request):
    if request.method == 'POST':
        id = check_session(request)
        if id == 0:
            return JsonResponse({'error': '-1', 'msg': '请先登录'})
        user_id = request.POST.get('user_id')
        comment_list = Comment.objects.filter(user_id=user_id)
        if comment_list:
            return JsonResponse({'error': '0', 'msg': '获取评论列表成功', 'data': [
                {
                    'achievement_id': comment.achievement_id,
                    'content': comment.content,
                    'create_time': comment.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                } for comment in comment_list
            ]})
        else:
            return JsonResponse({'error': '1002', 'msg': '评论列表为空'})
    else:
        return JsonResponse({'error': '1001', 'msg': '请求方式错误'})


# 获取某学术成果的评论数
@csrf_exempt  # 跨域设置
def get_comment_count_by_achievement(request):
    if request.method == 'POST':
        id = check_session(request)
        if id == 0:
            return JsonResponse({'error': '-1', 'msg': '请先登录'})
        achievement_id = request.POST.get('achievement_id')
        comment_count = Comment.objects.filter(achievement_id=achievement_id).count()
        return JsonResponse({'error': '0', 'msg': '获取评论数成功', 'data': comment_count})
    else:
        return JsonResponse({'error': '1001', 'msg': '请求方式错误'})


# 获取某用户评论的学术成果数
@csrf_exempt  # 跨域设置
def get_comment_count_by_user(request):
    if request.method == 'POST':
        id = check_session(request)
        if id == 0:
            return JsonResponse({'error': '-1', 'msg': '请先登录'})
        user_id = request.POST.get('user_id')
        comment_count = Comment.objects.filter(user_id=user_id).count()
        return JsonResponse({'error': '0', 'msg': '获取评论数成功', 'data': comment_count})
    else:
        return JsonResponse({'error': '1001', 'msg': '请求方式错误'})


# 收藏学术成果
@csrf_exempt  # 跨域设置
def collect_achievement(request):
    if request.method == 'POST':
        id = check_session(request)
        if id == 0:
            return JsonResponse({'error': '-1', 'msg': '请先登录'})
        achievement_id = request.POST.get('achievement_id')
        user_id = request.POST.get('user_id')
        collect = Collection.objects.filter(achievement_id=achievement_id, user_id=user_id)
        if collect:
            return JsonResponse({'error': '1003', 'msg': '已收藏'})
        else:
            collect = Collection.objects.create(achievement_id=achievement_id, user_id=user_id)
            if collect:
                return JsonResponse({'error': '0', 'msg': '收藏成功'})
            else:
                return JsonResponse({'error': '1002', 'msg': '收藏失败'})
    else:
        return JsonResponse({'error': '1001', 'msg': '请求方式错误'})


# 取消收藏学术成果
@csrf_exempt  # 跨域设置
def cancel_collect_achievement(request):
    if request.method == 'POST':
        id = check_session(request)
        if id == 0:
            return JsonResponse({'error': '-1', 'msg': '请先登录'})
        achievement_id = request.POST.get('achievement_id')
        user_id = request.POST.get('user_id')
        collect = Collection.objects.filter(achievement_id=achievement_id, user_id=user_id)
        if collect:
            collect.delete()
            return JsonResponse({'error': '0', 'msg': '取消收藏成功'})
        else:
            return JsonResponse({'error': '1003', 'msg': '未收藏'})
    else:
        return JsonResponse({'error': '1001', 'msg': '请求方式错误'})


# 获取某学术成果的收藏数
@csrf_exempt  # 跨域设置
def get_collect_count_by_achievement(request):
    if request.method == 'POST':
        id = check_session(request)
        if id == 0:
            return JsonResponse({'error': '-1', 'msg': '请先登录'})
        achievement_id = request.POST.get('achievement_id')
        collect_count = Collection.objects.filter(achievement_id=achievement_id).count()
        return JsonResponse({'error': '0', 'msg': '获取收藏数成功', 'data': collect_count})
    else:
        return JsonResponse({'error': '1001', 'msg': '请求方式错误'})


# 获取某用户收藏的学术成果数
@csrf_exempt  # 跨域设置
def get_collect_count_by_user(request):
    if request.method == 'POST':
        id = check_session(request)
        if id == 0:
            return JsonResponse({'error': '-1', 'msg': '请先登录'})
        user_id = request.POST.get('user_id')
        collect_count = Collection.objects.filter(user_id=user_id).count()
        return JsonResponse({'error': '0', 'msg': '获取收藏数成功', 'data': collect_count})
    else:
        return JsonResponse({'error': '1001', 'msg': '请求方式错误'})


# 获取某用户收藏的学术成果列表
@csrf_exempt  # 跨域设置
def get_collect_list_by_user(request):
    if request.method == 'POST':
        id = check_session(request)
        if id == 0:
            return JsonResponse({'error': '-1', 'msg': '请先登录'})
        user_id = request.POST.get('user_id')
        collect_list = Collection.objects.filter(user_id=user_id)
        if collect_list:
            return JsonResponse({'error': '0', 'msg': '获取收藏列表成功', 'data': [
                {
                    'achievement_id': collect.achievement_id,
                    'create_time': collect.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                } for collect in collect_list
            ]})
        else:
            return JsonResponse({'error': '1002', 'msg': '收藏列表为空'})
    else:
        return JsonResponse({'error': '1001', 'msg': '请求方式错误'})


# 获取学术成果的收藏列表
@csrf_exempt  # 跨域设置
def get_collect_list_by_achievement(request):
    if request.method == 'POST':
        id = check_session(request)
        if id == 0:
            return JsonResponse({'error': '-1', 'msg': '请先登录'})
        achievement_id = request.POST.get('achievement_id')
        collect_list = Collection.objects.filter(achievement_id=achievement_id)
        if collect_list:
            return JsonResponse({'error': '0', 'msg': '获取收藏列表成功', 'data': [
                {
                    'user_id': collect.user_id,
                    'create_time': collect.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                } for collect in collect_list
            ]})
        else:
            return JsonResponse({'error': '1002', 'msg': '收藏列表为空'})
    else:
        return JsonResponse({'error': '1001', 'msg': '请求方式错误'})


def index(request):
    # 通过设置时间戳，进行多次访问，可以看到时间戳的变化，就可以得知是否是缓存页面了
    return HttpResponse('当前时间戳：' + str(time.time()))
