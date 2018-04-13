# _*_ coding: utf-8 _*_
from random import Random
from users.models import EmailVerifyRecord

from django.conf import settings
from django.core.mail import send_mail

EMAIL_FROM = 'yaooooj@sina.com'


def send_register_email(email, send_type="register"):
    email_record = EmailVerifyRecord()
    code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    if send_type == "register":
        email_title = "暮学在线网注册链接"
        email_body = "请点击下面的链接激活你的账号：http://127.0.0.1:8000/active/{0}".format(code)

        send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, [email], fail_silently=False)
        return send_status


def random_str(randomlength=8):
    random_str = ' '
    chars = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        random_str += chars[random.randint(1, length)]
    return random_str