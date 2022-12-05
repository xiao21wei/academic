import datetime

from django.views.decorators.csrf import csrf_exempt
from my_app.models import *
from django.http import JsonResponse
from academic.tools import send_sms_code
import re

regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')


# 正则判断邮箱格式
def check_format_mail(email):
    if re.fullmatch(regex, email):
        return True
    return False


# 发送注册邮件
@csrf_exempt
def send_register_email(request):
    if request.method != 'POST':
        return JsonResponse({'error': '1001', 'msg': '请求方式错误'})
    email = request.POST.get('email')
    if not check_format_mail(email):
        return JsonResponse({'error': '1002', 'msg': '邮箱格式错误'})
    if User.objects.exists(email=email):
        return JsonResponse({'error': '1004', 'msg': '邮箱已被注册'})
    if send_sms_code(email, 'register'):
        return JsonResponse({'error': '0', 'msg': '邮件发送成功'})
    else:
        return JsonResponse({'error': '1003', 'msg': '邮件发送失败'})


# 判断验证码
def check_code(toemail, code):
    if VerificationCode.objects.exists(toemail):
        verificationcode = VerificationCode.objects.get(code=code, email=toemail)
        if (datetime.datetime.now() - verificationcode.time).seconds > 300:
            return 'wrong time'
        if code == verificationcode.code:
            return 'AC'
        else:
            return 'wrong'
    else:
        return 'not exist'


# 注册
@csrf_exempt
def register(request):
    if request.method != 'POST':
        return JsonResponse({'error': '1001', 'msg': '请求方式错误'})

    username = request.POST.get('username')
    if len(username) > 10 or len(username) < 2:
        return JsonResponse({'error': '1002', 'msg': '用户名在2-10个字符之间'})
    if User.objects.exists(name=username):
        return JsonResponse({'error': '1003', 'msg': '用户名已存在'})

    password = request.POST.get('password')
    password2 = request.POST.get('password2')
    if not password.isalnum:
        return JsonResponse({'error': '1004', 'msg': '密码只能由数字和大小写字母组成'})
    if len(password) > 18 or len(password) < 6:
        return JsonResponse({'error': '1005', 'msg': '密码长度需要为6-18位'})
    if password != password2:
        return JsonResponse({'error': '1006', 'msg': '两次密码不一致'})

    email = request.POST.get('email')
    if not check_format_mail(email):
        return JsonResponse({'error': '1007', 'msg': '邮箱格式错误'})
    if User.objects.exists(email=email):
        return JsonResponse({'error': '1011', 'msg': '邮箱已被注册'})
    code = request.POST.get('code')
    res = check_code(email, code)
    if res == 'wrong time':
        return JsonResponse({'error': '1008', 'msg': '验证码失效'})
    elif res == 'AC':
        realname = request.POST.get('realname')
        user = User(name=username, password=password, email=email, real_name=realname)
        user.save()
        return JsonResponse({'error': '0', 'msg': '注册成功'})
    elif res == 'wrong':
        return JsonResponse({'error': '1009', 'msg': '验证码错误'})
    else:
        return JsonResponse({'error': '1010', 'msg': '未获取验证码'})


# 登录
@csrf_exempt
def login(request):
    if request.method != 'POST':
        return JsonResponse({'error': '1001', 'msg': '请求方式错误'})

    if request.session.get('is_login', False):
        return JsonResponse({'error': '1002', 'msg': '用户已登录'})

    username = request.POST.get('username')
    password = request.POST.get('password')

    if not User.objects.exists(username=username):
        return JsonResponse({'error': '1003', 'msg': '用户名不存在'})

    if not User.objects.exists(username=username, password=password):
        return JsonResponse({'error': '1004', 'msg': '密码错误'})

    request.session['user'] = username
    request.session['is_login'] = True
    return JsonResponse({'error': '0', 'msg': '登录成功'})


# 登出
@csrf_exempt
def logout(request):
    request.session.flush()
    return JsonResponse({'error': '0', 'msg': '登出成功'})


# 获取个人信息
@csrf_exempt
def get_self_information(request):
    if request.method != 'GET':
        return JsonResponse({'error': '1001', 'msg': '请求方式错误'})
    if not request.session.get('is_login', False):
        return JsonResponse({'error': '1002', 'msg': '请先登录'})
    username = request.session.get('user')
    user = User.objects.get(username=username)
    return JsonResponse({'error': '0', 'msg': user})


# 获取他人信息
@csrf_exempt
def get_intro_by_username(request):
    if request.method != 'GET':
        return JsonResponse({'error': '1001', 'msg': '请求方式错误'})
    username = request.GET.get('username')
    if not User.objects.exists(username=username):
        return JsonResponse({'error': '1002', 'msg': '用户不存在'})
    user = User.objects.get(username=username)
    return JsonResponse({'error': '0', 'msg': user})


# 设置成为学者
@csrf_exempt
def set_scholar(request):
    if request.method != 'POST':
        return JsonResponse({'error': '1001', 'msg': '请求方式错误'})
    username = request.GET.get('username')
    user = User.objects.get(username=username)
    user.identity = 1
    user.save()
    return JsonResponse({'error': '0', 'msg': '设置成功'})


# 设置个人简介
@csrf_exempt
def set_intro(request):
    if request.method != 'POST':
        return JsonResponse({'error': '1001', 'msg': '请求方式错误'})
    intro = request.GET.get('intro')
    username = request.session.get('user')
    user = User.objects.get(username=username)
    user.intro = intro
    user.save()
    return JsonResponse({'error': '0', 'msg': '设置成功'})
