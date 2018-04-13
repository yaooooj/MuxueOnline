"""MxOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf.urls.static import static
from .settings import MEDIA_ROOT, MEDIA_URL
import xadmin

from users.views import LoginView, RegisterView, ActiveUserView,ForgetPasswordView
from organization.views import OrgView

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    path('index/', TemplateView.as_view(template_name="index.html"), name="index"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', TemplateView.as_view(template_name="login.html"), name="logout"),
    path('register/', RegisterView.as_view(), name="register"),
    path('captcha/', include('captcha.urls')),
    path('active/<int:active_code>', ActiveUserView.as_view(), name="active"),
    path('forgetpwd/', ForgetPasswordView.as_view(), name="forgetpwd"),


    # 授课机构
    path('org-list/', OrgView.as_view(), name="org-list"),
]
# 配置上传文件的访问地址
urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT,)