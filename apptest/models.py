from django.db import models
"""
 create table id(id,email,tag,password,name)
 create table student(stu_id,email,password)
 create table teacher(tea_id,email,password)
 create table course(course_id,course_name,teacher_id,credits,requirements)
 create table course_info(course_id,stu_id,att_points,exam_points)
 """
tag_choices = (
        (0,'管理员'),
        (1,'老师'),
        (2,'学生'))

class User(models.Model):
    user_id = models.IntegerField(verbose_name="用户ID",primary_key=True)    #verbose_name算是一个表中的注释
    email = models.CharField(verbose_name="用户邮箱",default="",null=True,blank=True)
    tag = models.SmallIntegerField(verbose_name="身份选择",choices=tag_choices)
    password = models.CharField(verbose_name="密码")
    name = models.CharField(verbose_name="姓名")
    
class Student(models.Model):
    stu_id = models.IntegerField(verbose_name="学生ID",primary_key=True)  # verbose_name算是一个表中的注释
    email = models.CharField(verbose_name="学生邮箱",default="",null=True,blank=True)
    name = models.CharField()


class Teacher(models.Model):
    tea_id = models.IntegerField(verbose_name="老师ID", primary_key=True)  # verbose_name算是一个表中的注释
    email = models.CharField(verbose_name="老师邮箱", default="",null=True,blank=True)
    name = models.CharField()


class Course(models.Model):
    course_id = models.IntegerField(verbose_name="课程ID", primary_key=True)  # verbose_name算是一个表中的注释
    course_name = models.CharField()
    teacher_id = models.IntegerField(verbose_name="老师ID")
    credits = models.IntegerField()
    requirements = models.CharField(default="",null=True,blank=True)

class Course_info(models.Model):
    course_id = models.IntegerField(verbose_name="课程ID")  # verbose_name算是一个表中的注释
    student_id = models.IntegerField(verbose_name="学生ID")
    attend_point = models.TextField(default="",null=True, blank=True)
    exam_point = models.TextField(default="",null=True, blank=True)
