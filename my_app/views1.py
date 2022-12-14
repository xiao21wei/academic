from django.views.decorators.csrf import csrf_exempt
from my_app.models import *
from django.http import JsonResponse
import re
from academic.settings import Redis
import os
from academic.settings import MEDIA_ROOT, IMG_URL
import random


# 简单检索
@csrf_exempt
def normal_search(request):
    if request.method != 'POST':
        return JsonResponse({'error': '1001', 'msg': '请求方式错误'})
    name = request.POST.get('name')
    author = request.POST.get('author')
    intro = request.POST.get('intro')
    area = request.POST.get('area')
    achievements = Achievement.objects.all()
    if name:
        achievements = achievements.filter(name__contains=name)
    if author:
        achievements = achievements.filter(author__contains='_'+author+'_')
    if intro:
        achievements = achievements.filter(intro__contains=intro)
    if area:
        achievements = achievements.filter(area__contains='_'+area+'_')
    if not achievements.first():
        return JsonResponse({'error': '1002', 'msg': '没有检索到学术成果'})
    articles = []
    for achievement in achievements.order_by('-create_time'):
        # authors = []
        # author = {'affiliation_id': '4654613', 'affiliation_name': '', 'affiliation_order': 1, 'author': '2411226248',
        #           'author_name': 'Adam Paszke', 'order': "1"}
        # authors.append(author)
        authors = []
        for author_name in list(filter(None, achievement.author.split('_'))):
            affiliation_id = ''
            affiliation_name = ''
            author_id = ''
            if User.objects.filter(real_name=author_name).exists():
                author = User.objects.filter(real_name=author_name).first()
                author_id = str(author.user_id)
                if Team.objects.filter(team_id=author.team_id).exists():
                    team = Team.objects.filter(team_id=author.team_id).first()
                    affiliation_id = str(team.team_id)
                    affiliation_name = team.name
            authors.append({
                'affiliation_id': affiliation_id,
                'affiliation_name': affiliation_name,
                'affiliation_order': 1,
                'author_id': author_id,
                'author_name': author_name,
                'order': ""
            })
        # fields = []
        # field = {'citation_count': 0, 'field_id': '', 'level': 1, 'main_type': '', 'name': area, 'paper_count': 0,
        #          'rank': 0}
        # fields.append(field)
        fields = [{
            'citation_count': 0,
            'field_id': '',
            'level': 1,
            'main_type': '',
            'name': area,
            'paper_count': 0,
            'rank': 0
        } for area in list(filter(None, achievement.area.split('_')))]
        article = {'author_affiliation': [], 'authors': authors, 'fields': fields,
                   'paper_id': str(achievement.achievement_id), 'paper_title': achievement.name, 'abstract': achievement.intro,
                   'citation_count': 0, 'comment_count': 0, 'year': 2022, 'reference_count': 0, 'is_collect': True, }

        articles.append(article)
    return JsonResponse({'error': '0', 'msg': '获取学术成果成功', 'len': len(achievements), 'articles': articles})


@csrf_exempt
def file_upload(request):
    if request.method != 'POST':
        return JsonResponse({'error': '1001', 'msg': '请求方式错误'})
    file = request.FILES.get("file")
    if file.name in os.listdir(MEDIA_ROOT):
        filename = os.path.join(MEDIA_ROOT, str(random.randint(0, 100) * random.randint(0, 100) - random.randint(0, 5)) + file.name)
    else:
        filename = os.path.join(MEDIA_ROOT, file.name)
    print(f"文件所在地址为：{filename}")
    with open(filename, 'wb') as f:
        f.write(file.file.read())
    # 获取文件的绝对地址
    file_path = IMG_URL +'home/academic/img/'+file.name
    return JsonResponse({'error': '0', 'msg': '上传成功', 'url': file_path, 'file_path': file_path})


@csrf_exempt
def search_info(request):
    if request.method != 'POST':
        return JsonResponse({'error': '1001', 'msg': '请求方式错误'})
    author_id = request.POST.get('author_id')
    achievements = Achievement.objects.all()
    affiliation = '暂无机构'
    if User.objects.filter(user_id=author_id).exists():
        user = User.objects.filter(user_id=author_id).first()
        author_name = user.real_name
        if Team.objects.filter(team_id=user.team_id).exists():
            affiliation = Team.objects.filter(team_id=user.team_id).first().name
    else:
        return JsonResponse({'error': '1002', 'msg': '用户不存在'})

    if author_id:
        achievements = achievements.filter(author__contains='_'+author_name+'_')
    # if not achievements.first():
    #     return JsonResponse({'error': '0', 'msg': '没有检索到学术成果'})
    articles = []
    for achievement in achievements.order_by('-create_time'):
        # authors = []
        # author = {'affiliation_id': '4654613', 'affiliation_name': '', 'affiliation_order': 1, 'author': '2411226248',
        #           'author_name': 'Adam Paszke', 'order': "1"}
        # authors.append(author)
        authors = []
        for author_name in list(filter(None, achievement.author.split('_'))):
            affiliation_id = ''
            affiliation_name = ''
            author_id = ''
            if User.objects.filter(real_name=author_name).exists():
                author = User.objects.filter(real_name=author_name).first()
                author_id = str(author.user_id)
                if Team.objects.filter(team_id=author.team_id).exists():
                    team = Team.objects.filter(team_id=author.team_id).first()
                    affiliation_id = str(team.team_id)
                    affiliation_name = team.name
            authors.append({
                'affiliation_id': affiliation_id,
                'affiliation_name': affiliation_name,
                'affiliation_order': 1,
                'author_id': author_id,
                'author_name': author_name,
                'order': ""
            })
        # fields = []
        # field = {'citation_count': 0, 'field_id': '', 'level': 1, 'main_type': '', 'name': area, 'paper_count': 0,
        #          'rank': 0}
        # fields.append(field)
        fields = [{
            'citation_count': 0,
            'field_id': '',
            'level': 1,
            'main_type': '',
            'name': area,
            'paper_count': 0,
            'rank': 0
        } for area in list(filter(None, achievement.area.split('_')))]
        article = {'author_affiliation': [], 'authors': authors, 'fields': fields,
                   'paper_id': str(achievement.achievement_id), 'paper_title': achievement.name, 'abstract': achievement.intro,
                   'citation_count': Like.objects.filter(achievement_id=achievement.achievement_id).count(),
                   'comment_count': 0, 'year': 2022, 'reference_count': 0, 'is_collect': True,
                   'date': achievement.create_time.date(), }

        articles.append(article)

    return JsonResponse({'error': '0', 'msg': '获取学术成果成功', 'len': len(achievements), 'articles': articles,
                         'people': {'author_name': user.real_name, 'affiliation': affiliation, 'email': user.email}})


@csrf_exempt
def authentication(request):
    if request.method != 'POST':
        return JsonResponse({'error': '1001', 'msg': '请求方式错误'})
    affiliation = request.POST.get('affiliation')
    user_id = request.POST.get('user_id')
    if not User.objects.filter(user_id=user_id).exists():
        return JsonResponse({'error': '1002', 'msg': '用户不存在'})
    if not Team.objects.filter(name=affiliation).exists():
        return JsonResponse({'error': '1003', 'msg': '团队不存在'})
    user = User.objects.filter(user_id=user_id).first()
    team = Team.objects.filter(name=affiliation).first()
    user.team_id = team.team_id
    user.save()
    return JsonResponse({'error': '0', 'msg': '认证成功'})
