from academic.tools import check_session
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
import random


# 发送私聊-保存
@csrf_exempt  # 跨域设置
def send_chat(request):  # 不要给自己发送消息
    if request.method == 'POST':
        content = request.POST.get('content')
        receive = request.POST.get('receive')
        id = check_session(request)
        if id == 0:
            return JsonResponse({'error': '-1', 'msg': '请先登录'})
        send = id
        if receive == send:
            return JsonResponse({'error': '1002', 'msg': '无法给自己发消息'})

        chat = Chat(send=send, receive=receive, content=content)
        chat.save()

        return JsonResponse({'error': '0', 'msg': '私聊发送成功'})
    else:
        return JsonResponse({'error': '1001', 'msg': '请求方式错误'})


@csrf_exempt  # 跨域设置
def receive_chat(request):  # 收到之前未收到的的消息
    if request.method == 'POST':
        id = check_session(request)
        if id == 0:
            return JsonResponse({'error': '-1', 'msg': '请先登录'})
        receive = id
        send = request.POST.get('send')
        all_chat = list()
        num = Chat.objects.filter(receive=receive, send=send).count()
        if num >= 2:
            chat_list = list(Chat.objects.filter(receive=receive, send=send, received=False).order_by('send_time'))

            for chat in chat_list:
                content_time = {
                    'time': chat.send_time,
                    'content': chat.content,
                }
                all_chat.append(content_time)
                chat.received = True
                chat.save()
        else:  # 仅一条的情况
            chat = Chat.objects.get(receive=receive, send=send)

            all_chat = {
                'time': chat.send_time,
                'content': chat.content,
            }
            chat.received = True
            chat.save()

        return JsonResponse({'error': '0', 'msg': '私聊内容及时间为  ' + all_chat})
    else:
        return JsonResponse({'error': '1001', 'msg': '请求方式错误'})


@csrf_exempt  # 跨域设置
def chat_history(request):  # 两人所有的聊天记录
    if request.method == 'POST':
        receive = request.POST.get('receive')
        send = request.POST.get('send')
        all_chat = list()
        num = Chat.objects.filter(Q(receive=receive) | Q(receive=send), Q(send=send) | Q(send=receive)).count()
        if num >= 2:
            chat_list = list(Chat.objects.filter(Q(receive=receive) | Q(receive=send), Q(send=send) | Q(send=receive))
                             .order_by('send_time'))

            for chat in chat_list:
                content_time = {
                    'send': chat.send,
                    'receive': chat.receive,
                    'time': chat.send_time,
                    'content': chat.content,
                }
                all_chat.append(content_time)
        else:  # 仅一条的情况
            chat = Chat.objects.get(receive=receive, send=send)

            content_time = {
                'send': chat.send,
                'receive': chat.receive,
                'time': chat.send_time,
                'content': chat.content,
            }
            all_chat.append(content_time)

        return JsonResponse({'error': '0', 'msg': '两人全部聊天记录为  ' + all_chat})
    else:
        return JsonResponse({'error': '1001', 'msg': '请求方式错误'})


# 队长建立队伍
@csrf_exempt  # 跨域设置
def create_team(request):
    if request.method == 'POST':
        id = check_session(request)
        if id == 0:
            return JsonResponse({'error': '-1', 'msg': '请先登录'})
        # 队伍名称
        name = request.POST.get('name')
        intro = request.POST.get('intro')
        nowuser = User.objects.get(user_id=id)

        team = Team(name=name, intro=intro, user_list=id)
        team.save()  # 保存到数据库
        nowuser.team_id = team.team_id
        nowuser.save()
        return JsonResponse({'error': '0', 'msg': '队伍建立成功'})
    else:
        return JsonResponse({'error': '1001', 'msg': '请求方式错误'})


# 邀请成员，队伍中的每个人都可以邀请成员
@csrf_exempt  # 跨域设置
def invite_member(request):
    if request.method == 'POST':
        id = check_session(request)
        if id == 0:
            return JsonResponse({'error': '-1', 'msg': '请先登录'})
        # 被邀请成员id
        invite_id = request.post.get('invited_id')
        invite_user = User.objects.get(user_id=invite_id)
        if invite_user.team_id != 'NULL':
            return JsonResponse({'error': '1002', 'msg': '被邀请成员已有团队'})
        #
        nowuser = User.objects.get(user_id=id)
        if nowuser.team_id == 'NULL':
            return JsonResponse({'error': '1003', 'msg': '发出邀请者必须已有团队'})
        team = Team.objects.get(team_id=nowuser.team_id)
        invite_user.team_id = team.team_id
        team.user_list = team.user_list + ',' + invite_id
        team.save()  # 保存到数据库
        invite_user.save()
        return JsonResponse({'error': '0', 'msg': '邀请成功'})
    else:
        return JsonResponse({'error': '1001', 'msg': '请求方式错误'})


# 队长更改简介
@csrf_exempt  # 跨域设置
def change_intro(request):
    if request.method == 'POST':
        id = check_session(request)
        if id == 0:
            return JsonResponse({'error': '-1', 'msg': '请先登录'})
        intro = request.post.get('intro')
        nowuser = User.objects.get(user_id=id)
        if nowuser.team_id == 'NULL':
            return JsonResponse({'error': '1002', 'msg': '您没有团队'})
        team = Team.objects.get(team_id=nowuser.team_id)
        namelist = team.user_list.split(',')
        leader = namelist[0]
        if leader != id:
            return JsonResponse({'error': '1003', 'msg': '您不是队长'})
        team.intro = intro
        team.save()
        return JsonResponse({'error': '0', 'msg': '更改成功'})
    else:
        return JsonResponse({'error': '1001', 'msg': '请求方式错误'})


# 热门文章
@csrf_exempt  # 跨域设置
def hot_achievement(request):
    if request.method == 'POST':

        # 返回3篇
        achievements = Achievement.objects.all().order_by('-hot')[:3]
        top_articles = list()
        for achieve in achievements:
            order = 0
            order = order + 1

            authors = [{
                'affiliation_id': '',
                'affiliation_name': '',
                'affiliation_order': 1,
                'author_id': '',
                'author_name': author_name,
                'order': str(order)
            } for author_name in list(filter(None, achieve.author.split('_')))]

            firre = {
                'authors': authors,
                'book_title': "book title",
                'citation_count': Like.objects.filter(achievement_id=achieve.achievement_id).count(),
                'citation_msg': [],
                'conference': {
                    'name': "conference name",
                },
                'collect_num': Collection.objects.filter(achievement_id=achieve.achievement_id).count(),
                'conference_id': "",
                'date': achieve.create_time.date(),
                'doctype': 'doctype',
                'fields': [achieve.area],
                'first_page': "123",
                'journal': {
                    'citation_count': str(random.randint(0, 17)),
                    'issn': "",
                    'journalid': str(achieve.achievement_id),
                    'name': achieve.name,
                    'paper_count': "13",
                    'publisher': "publisher",
                    'rank': "1",
                    'webpage': "",
                },
                'journal_id': str(achieve.achievement_id),
                'last_page': "12345",
                'paper_id': str(achieve.achievement_id),
                'paper_title': achieve.name,
                'publisher': "publisher",
                'rank': "1",
                'reference_count': "2",
                'volumn': "10",
                'year': achieve.create_time.year,
                'abstract': achieve.intro
            }

            top_articles.append(firre)

        if achievements:
            return JsonResponse({'error': '0', 'msg': '获取热门学术成果成功', 'top_articles': top_articles, 'data': [
                {
                    'achievement_id': achievement.achievement_id,
                    'like': Like.objects.filter(achievement_id=achievement.achievement_id).count(),
                    'collection': Collection.objects.filter(achievement_id=achievement.achievement_id).count(),
                    'name': achievement.name,
                    # 用'_'分割字符串，去除空，返回列表
                    'authors': list(filter(None, achievement.author.split('_'))),
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


# 推荐文章
@csrf_exempt  # 跨域设置
def recommend_achievement(request):
    if request.method == 'POST':
        # 返回3篇
        achievements = Achievement.objects.all().order_by('-recommend')[:3]
        top_articles = list()
        for achieve in achievements:
            order = 0
            order = order + 1

            authors = [{
                'affiliation_id': '',
                'affiliation_name': '',
                'affiliation_order': 1,
                'author_id': '',
                'author_name': author_name,
                'order': str(order)
            } for author_name in list(filter(None, achieve.author.split('_')))]

            firre = {
                'authors': authors,
                'book_title': "book title",
                'citation_count': Like.objects.filter(achievement_id=achieve.achievement_id).count(),
                'citation_msg': [],
                'conference': {
                    'name': "conference name"
                },
                'collect_num': Collection.objects.filter(achievement_id=achieve.achievement_id).count(),
                'conference_id': "",
                'date': achieve.create_time.date(),
                'doctype': 'doctype',
                'fields': [achieve.area],
                'first_page': "123",
                'journal': {
                    'citation_count': str(random.randint(0, 17)),
                    'issn': "",
                    'journalid': str(achieve.achievement_id),
                    'name': achieve.name,
                    'paper_count': "13",
                    'publisher': "publisher",
                    'rank': "1",
                    'webpage': "",
                },
                'journal_id': str(achieve.achievement_id),
                'last_page': "12345",
                'paper_id': str(achieve.achievement_id),
                'paper_title': achieve.name,
                'publisher': "publisher",
                'rank': "1",
                'reference_count': "2",
                'volumn': "10",
                'year': achieve.create_time.year,
                'abstract': achieve.intro
            }

            top_articles.append(firre)

        if achievements:
            return JsonResponse({'error': '0', 'msg': '获取推荐学术成果成功', 'top_articles': top_articles, 'data': [
                {
                    'achievement_id': achievement.achievement_id,
                    'like': Like.objects.filter(achievement_id=achievement.achievement_id).count(),
                    'collection': Collection.objects.filter(achievement_id=achievement.achievement_id).count(),
                    'name': achievement.name,
                    # 用'_'分割字符串，去除空，返回列表
                    'authors': list(filter(None, achievement.author.split('_'))),
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