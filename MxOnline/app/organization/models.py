# -*- coding: utf-8 -*-
from datetime import datetime

from django.db import models

# Create your models here.


class CityDict(models.Model):
    name = models.CharField(max_length=20, verbose_name=u"城市")
    desc = models.CharField(max_length=20, verbose_name=u"城市描述")
    add_time = models.DateField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"城市"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseOrg(models.Model):
    name = models.CharField(max_length=20, verbose_name=u"机构名称")
    desc = models.TextField(max_length=20, verbose_name=u"机构描述")
    category = models.CharField(max_length=20, verbose_name=u"类别", choices=(("pxjg", "培训机构"), ("gr", "个人"), ("gx", "高校")), default="pxjg")
    click_nums = models.IntegerField(default=0, verbose_name=u"点击次数")
    fav_nums = models.IntegerField(default=0, verbose_name=u"收藏人数")
    image = models.ImageField(upload_to="image/%Y/%m", default=u"image/default.png", max_length=100, verbose_name=u"封面")
    address = models.CharField(max_length=50, verbose_name=u"机构地址")
    city = models.ForeignKey(CityDict, verbose_name=u"所在城市", on_delete=models.CASCADE)
    students = models.IntegerField(default=0, verbose_name=u"学习人数")
    course_num = models.IntegerField(default=0, verbose_name=u"课程数")
    add_time = models.DateField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"课程机构"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Teacher(models.Model):
    org = models.ForeignKey(CourseOrg, verbose_name=u"所属机构", on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name=u"教师名")
    work_year = models.IntegerField(default=0, verbose_name=u"工作年限")
    work_company = models.CharField(max_length=50, verbose_name=u"就职公司")
    work_position = models.CharField(max_length=50, verbose_name=u"公司职位")
    points = models.CharField(max_length=50, verbose_name=u"教学特点")
    click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
    fav_nums = models.IntegerField(default=0, verbose_name=u"收藏数")
    image = models.ImageField(upload_to="image/%Y/%m", default=u"image/default.png", max_length=100, verbose_name=u"头像", null=True, blank=True)
    teacher_c_num = models.IntegerField(default=0, verbose_name=u"讲师课程数")
    is_valid = models.CharField(default='wrz', verbose_name=u"是否已认证", choices=(("rz", "已认证"), ("wrz", "未认证")),
                                max_length=5)
    add_time = models.DateField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"教师"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name