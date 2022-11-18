from django.shortcuts import render
from my_app.models import *
from django.http import JsonResponse


# Path: my_app\urls.py
# Create your views here.
def publish_achievement(request):
    if request.method == 'POST':
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


def get_achievement(request):
    if request.method == 'POST':
        achievement_id = request.GET.get('achievement_id')
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


def get_achievements(request):
    if request.method == 'POST':
        achievements = Achievement.objects.all()
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
                } for achievement in achievements
            ]})
        else:
            return JsonResponse({'error': '1002', 'msg': '学术成果不存在'})
    else:
        return JsonResponse({'error': '1001', 'msg': '请求方式错误'})


def update_achievement(request):
    if request.method == 'POST':
        achievement_id = request.POST.get('achievement_id')
        user_id = request.POST.get('user_id')
        achievement = Achievement.objects.get(achievement_id=achievement_id)
        if achievement:
            # 获取author_id的第一个值，即为作者id
            author_id = achievement.author_id.split('_')[0]
            if author_id == user_id:
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


def delete_achievement(request):
    if request.method == 'POST':
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


def get_achievements_by_area(request):
    if request.method == 'POST':
        area = request.GET.get('area')
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
                } for achievement in achievements
            ]})
        else:
            return JsonResponse({'error': '1002', 'msg': '学术成果不存在'})
    else:
        return JsonResponse({'error': '1001', 'msg': '请求方式错误'})


def get_achievements_by_type(request):
    if request.method == 'POST':
        type = request.GET.get('type')
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
                } for achievement in achievements
            ]})
        else:
            return JsonResponse({'error': '1002', 'msg': '学术成果不存在'})
    else:
        return JsonResponse({'error': '1001', 'msg': '请求方式错误'})


def get_achievements_by_name(request):
    if request.method == 'POST':
        name = request.GET.get('name')
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
                } for achievement in achievements
            ]})
        else:
            return JsonResponse({'error': '1002', 'msg': '学术成果不存在'})
    else:
        return JsonResponse({'error': '1001', 'msg': '请求方式错误'})


def get_achievements_by_author(request):
    if request.method == 'POST':
        author = request.GET.get('author')
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
                } for achievement in achievements
            ]})
        else:
            return JsonResponse({'error': '1002', 'msg': '学术成果不存在'})
    else:
        return JsonResponse({'error': '1001', 'msg': '请求方式错误'})


# 根据时间范围查找学术成果
def get_achievements_by_time(request):
    if request.method == 'POST':
        start_time = request.GET.get('start_time')
        end_time = request.GET.get('end_time')
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
                } for achievement in achievements
            ]})
        else:
            return JsonResponse({'error': '1002', 'msg': '学术成果不存在'})
    else:
        return JsonResponse({'error': '1001', 'msg': '请求方式错误'})



