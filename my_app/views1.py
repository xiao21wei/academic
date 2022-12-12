from django.views.decorators.csrf import csrf_exempt

from academic.tools import check_session
from my_app.models import *
from django.http import JsonResponse
import re
from academic.settings import Redis


# 简单检索
@csrf_exempt
def normal_search(request):
    if request.method != 'POST':
        return JsonResponse({'error': '1001', 'msg': '请求方式错误'})
    id = check_session(request)
    if id == 0:
        return JsonResponse({'error': '-1', 'msg': '请先登录'})
    title = request.POST.get('title')
    author = request.POST.get('author')
    abstract = request.POST.get('abstract')
    area = request.POST.get('area')
    achievements = Achievement.objects.all()
    if len(title) > 0:
        achievements = Achievement.objects.filter(name__contains=title)
    if len(author) > 0:
        author_id = User.objects.get(real_name=author).user_id
        achievements = Achievement.objects.filter(author_id__contains='_'+author_id+'_')
    if len(abstract) > 0:
        achievements = Achievement.objects.filter(intro__contains=abstract)
    if len(area) > 0:
        achievements = Achievement.objects.filter(area__contains='_'+area+'_')
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
        return JsonResponse({'error': '1002', 'msg': '没有检索到学术成果'})
