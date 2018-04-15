# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import CourseOrg, CityDict
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