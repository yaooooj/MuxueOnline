# -*- coding: utf-8 -*-
import json

from django.shortcuts import render, HttpResponse
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


from .models import CourseOrg, CityDict, Teacher
from operation.forms import UserAskForm
from course.models import Course
from operation.models import UserFavorite
# Create your views here.


class OrgView(View):
    @staticmethod
    def get(request):
        all_orgs = CourseOrg.objects.all()
        hot_orgs = all_orgs.order_by('-click_nums')[:3]
        all_citys = CityDict.objects.all()

        # 筛选城市
        city_id = request.GET.get('city', "")
        if city_id:
            all_orgs = CourseOrg.objects.filter(city_id=int(city_id))

        # 机构筛选
        category = request.GET.get('org', "")
        if category:
            all_orgs = CourseOrg.objects.filter(category=category)

        # 筛选城市和机构
        if city_id and category:
            all_orgs = CourseOrg.objects.filter(city_id=int(city_id), category=category)

        # 按照学习人数或课程数排序
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "students":
                all_orgs = all_orgs.order_by('-students')
            elif sort == "course":
                all_orgs = all_orgs.order_by('-course_num')

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(all_orgs, 2, request=request)
        count = p.count
        orgs = p.page(page)

        return render(request, "org-list.html", {
            "all_orgs": orgs,
            "all_citys": all_citys,
            "count": count,
            "city_id": city_id,
            "category": category,
            "hot_orgs": hot_orgs,
            "sort": sort,
        })


class AddAskView(View):
    @staticmethod
    def post(request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            response = {'status': 'success'}
            return HttpResponse(json.dumps(response), content_type='application/json')
        else:
            response = {'status': 'fail', 'msg': '添加出错'}
            return HttpResponse(json.dumps(response), content_type='application/json')


class TeacherView(View):
    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_teachers = course_org.teacher_set.all()
        return render(request, 'org-detail-teachers.html', {
            "all_teachers": all_teachers,
            "course_org": course_org,
        })


class HomePageView(View):
    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:1]
        return render(request, 'org-detail-homepage.html', {
            "all_courses": all_courses,
            "all_teachers": all_teachers,
            "course_org": course_org,
        })


class DescView(View):
    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        return render(request, 'org-detail-desc.html', {
            "course_org": course_org,
        })


class CourseView(View):
    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()
        return render(request, 'org-detail-course.html', {
            "all_courses": all_courses,
            "course_org": course_org,
        })


class AddFavView(View):
    def post(self, request):
        fav_id = request.POST.get('fav_id', '')
        fav_type = request.POST.get('fav_type', '')

        if not request.user.is_authenticated():
            # 判断用户登录状态
            response = {'status': 'fail', 'msg': u'用户未登录'}
            return HttpResponse(json.dumps(response), content_type='application/json')

        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_records:
            exist_records.delete()
            response = {'status': 'success', 'msg': '收藏'}
            return HttpResponse(json.dumps(response), content_type='application/json')
        else:
            user_fav = UserFavorite
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()
                response = {'status': 'success', 'msg': '已收藏'}
                return HttpResponse(json.dumps(response), content_type='application/json')
            else:
                response = {'status': 'fail', 'msg': '收藏出错'}
                return HttpResponse(json.dumps(response), content_type='application/json')