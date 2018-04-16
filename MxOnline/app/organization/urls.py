# _*_ coding: utf-8 _*_

from django.urls import path
from .views import OrgView, AddAskView, TeacherView, HomePageView, CourseView, DescView, AddFavView

app_name = 'organization'
urlpatterns = [

    # 授课机构
    path('list/', OrgView.as_view(), name="org_list"),
    path('add_ask/', AddAskView.as_view(), name="add_ask"),
    path('homepage/<str:org_id>/', HomePageView.as_view(), name="homepage"),
    path('teacher/<str:org_id>/', TeacherView.as_view(), name="teacher"),
    path('course/<str:org_id>/', CourseView.as_view(), name="course"),
    path('desc/<str:org_id>/', DescView.as_view(), name="desc"),

    # 机构收藏
    path('add_fav/', AddFavView.as_view(), name="add_fav"),
]