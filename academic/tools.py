import random

from django.core.mail import EmailMessage
from django.core.mail import send_mail  # 发送邮件模块
from django.conf import settings  # setting.py添加的的配置信息
from django.template import loader

from my_app.models import VerificationCode


def random_code():
    lis = []
    res1 = ""
    for i in range(6):
        num = random.randint(0, 9)
        res1 += str(num)
    lis.append(res1)
    return res1


def send_sms_code(to_mail, send_type):
    # 生成邮箱验证码
    code = random_code()

    if send_type == 'register':
        email_title = "用户注册验证"

    elif send_type == 'forget':
        email_title = "用户密码重置"

    elif send_type == 'update_password':
        email_title = "用户密码修改"

    else:
        return False

    context = {'code1': code[0],
               'code2': code[1],
               'code3': code[2],
               'code4': code[3],
               'code5': code[4],
               'code6': code[5]}
    email_template_name = 'code_mail.html'
    t = loader.get_template(email_template_name)
    html_content = t.render(context)

    msg = EmailMessage(email_title, html_content, settings.EMAIL_FROM, [to_mail])
    msg.content_subtype = 'html'
    send_status = msg.send()
    if send_status:
        if VerificationCode.objects.filter(email=to_mail).exists():
            VerificationCode.objects.filter(email=to_mail).delete()
        VerificationCode.objects.create(email=to_mail, code=code)
        return True
    else:
        return False


def check_session(request):
    id = request.session.get('user', 0)
    return id
