"""
URL configuration for django_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from apptest import views

urlpatterns = [
    path("",views.login),
    path("login/",views.login),
    path("index/manager",views.index_manager),
    path("index/manager/adduser",views.adduser),
    path("index/manager/deluser/",views.deluser),
    path("index/manager/<int:nid>/edit/",views.edituser),
    path("index/manager/addcourse",views.addcourse),
    path("index/manager/delcourse/",views.delcourse),
    path("index/manager/courseseek",views.courseseek),
    path("index/manager/<int:nid>/editcourse",views.editcourse),
    path("index/manager/<int:nid>/courseinfo",views.course_info),
    path("index/manager/<int:nid>/addcourseinfo",views.addcourse_info),
    path("index/manager/<int:nid>/delcourseinfo/",views.delcourse_info),
    path("index/student", views.index_student),
    path("index/student/email", views.stu_email),
    path("index/student/password", views.stu_password),
    path("index/teacher", views.index_teacher),
    path("index/teacher/<int:nid>/editpoint",views.editpoint),
    path("index/teacher/email", views.tea_email),
    path("index/teacher/password", views.tea_password),
    path("table/",views.tables),
    #path("add/user",views.adduser),
    #path("add/stu",views.addstu),
    #path("add/tea",views.addtea),
    #path("add/cou",views.addcou),
    #path("del/user",views.deluser),
    #path("del/stu",views.delstu),
    #path("del/tea",views.deltea),
    #path("del/cou",views.delcou),
    #path("stu/check")
]
