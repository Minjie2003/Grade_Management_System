from typing import List, Any

from django.shortcuts import render,HttpResponse,redirect
from apptest import models
# Create your views here.
from django import forms
from django.db.models import Q
from django.utils.safestring import mark_safe
class Loginform(forms.Form):
    user_id = forms.IntegerField(
        label="用户id",
        widget=forms.NumberInput(attrs={"class": "input-material","step": "any","type": "tel"}),
        required = True
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(attrs={"class": "input-material"}),
        required=True
    )

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label="旧密码", widget=forms.PasswordInput(attrs={"class":"input-material form-control"}))
    new_password = forms.CharField(label="新密码", widget=forms.PasswordInput(attrs={"class":"input-material form-control"}))
    confirm_password = forms.CharField(label="确认新密码", widget=forms.PasswordInput(attrs={"class":"input-material form-control"}))

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password != confirm_password:
            raise forms.ValidationError("新密码和确认密码不一致")

        return cleaned_data

class ChangeEmailForm(forms.Form):
    old_email = forms.CharField(
        label="旧邮箱",
        widget=forms.EmailInput(attrs={"class":"input-material form-control"}),
        required=False
    )
    new_email = forms.CharField(
        label="新邮箱",
        widget=forms.EmailInput(attrs={"class":"input-material form-control"}),
        required=True
    )
    confirm_email=forms.CharField(
        label="确认新邮箱",
        widget=forms.EmailInput(attrs={"class": "input-material form-control"}),
        required=True
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_email")
        confirm_password = cleaned_data.get("new_email")

        if new_password != confirm_password:
            raise forms.ValidationError("新邮箱和确认邮箱不一致")
        return cleaned_data

def login(request):
    form = Loginform()
    if request.method == "GET":
        return render(request,"login.html",{"form":form})
    elif request.method == "POST":
        form = Loginform(data=request.POST)
        if form.is_valid():
            # 验证数据是否存在
            admin_object = models.User.objects.filter(**form.cleaned_data).first()
            if not admin_object:
                # 添加错误信息
                form.add_error("password", "用户名或密码错误")
                return render(request, "login.html", {"form": form})
            else:
                request.session["info"] = {'user_id': admin_object.user_id, 'name':admin_object.name,'password': admin_object.password}
                if admin_object.tag == 0:
                    return redirect("/index/manager")
                elif admin_object.tag == 1:
                    return redirect("/index/teacher")
                elif admin_object.tag == 2:
                    return redirect("/index/student")
        return render(request, "login.html", {"form": form})

def index_manager(request):
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        if search_data == "管理员":
            query_condition = Q(tag__contains=0)
        elif search_data == "老师":
            query_condition = Q(tag__contains=1)
        elif search_data == "学生":
            query_condition = Q(tag__contains=2)
        else:
            query_condition = Q(user_id__contains=search_data) | Q(name__contains=search_data)
        data_dict['query_condition'] = query_condition
    else:
        # 如果 search_data 不存在，则默认查询条件为空
        data_dict['query_condition'] = Q()

    # 使用 get 方法获取 'query_condition' 键对应的值，如果不存在则为默认值 Q()
    query_condition = data_dict.get('query_condition')

    # 这里选择需要展示的字段，不使用 '__contains'
    queryset = models.User.objects.filter(query_condition)
    user_count = models.Course.objects.all().count()
    man_num=0
    tea_num=0
    stu_num=0
    for obj in queryset:
        if obj.tag == 0:
            man_num = man_num+1
        elif obj.tag == 1:
            tea_num = tea_num+1
        elif obj.tag == 2:
            stu_num = stu_num+1
    # 获取当前页码page，无指定的数即返回1
    page = int(request.GET.get('page', '1'))
    # 页码范围，一页多少个
    page_size = 10
    # 开始的页码和结束的页码
    start = (page - 1) * page_size
    end = page * page_size
    # queryset为当前页的数据
    queryset = models.User.objects.filter(query_condition).order_by("user_id")[start:end]
    # 总的条数
    total_count = models.User.objects.filter(query_condition).order_by("user_id").count()
    # 获取要分多少个页以及页尾有多少个条数
    total_page_count, div = divmod(total_count, page_size)
    # 如果页尾为空的话，页数+1
    if div:
        total_page_count += 1
    # 前端页面中可见的页数
    visible_pages = 5
    if total_page_count <= visible_pages * 2 + 1:
        start_page = 1
        end_page = total_page_count
    else:
        if page <= visible_pages:
            start_page = 1
            end_page = page + visible_pages
        elif page >= total_page_count - visible_pages:
            start_page = page - visible_pages
            end_page = total_page_count
        else:
            start_page = page - visible_pages
            end_page = page + visible_pages

    # 设置一个空列表，用在前端写对应的页码
    page_str_list = []
    ele = '<li class="page-item"><a class="page-link" href="?page={}">首页</a></li>'.format(1)
    page_str_list.append(ele)
    if page > 1:
        ele = '<li class="page-item"><a class="page-link" href="?page={}">上一页</a></li>'.format(page - 1)
        page_str_list.append(ele)
    for i in range(start_page, end_page + 1):
        if i == page:
            ele = '<li class="page-item active"><a class="page-link" href="?page={}">{}</a></li>'.format(i, i)
        else:
            ele = '<li class="page-item"><a class="page-link" href="?page={}">{}</a></li>'.format(i, i)
        page_str_list.append(ele)
    if page < total_page_count:
        ele = '<li class="page-item"><a class="page-link" href="?page={}">下一页</a></li>'.format(page + 1)
        page_str_list.append(ele)
    ele = '<li class="page-item"><a class="page-link" href="?page={}">尾页</a></li>'.format(total_page_count)
    page_str_list.append(ele)
    page_string = mark_safe("".join(page_str_list))
    return render(request, "index_manager.html", {'queryset': queryset,'man_num':man_num,'tea_num':tea_num,'stu_num':stu_num,
                                                  'user_count':user_count,"search_data": search_data, "page_string": page_string})

def adduser(request):
    if request.method == "GET":
        queryset = models.User.objects.all()
        user_count = models.Course.objects.all().count()
        man_num = 0
        tea_num = 0
        stu_num = 0
        for obj in queryset:
            if obj.tag == 0:
                man_num = man_num + 1
            elif obj.tag == 1:
                tea_num = tea_num + 1
            elif obj.tag == 2:
                stu_num = stu_num + 1
        return render(request,"adduser.html",{'queryset': queryset,'man_num':man_num,'tea_num':tea_num,'stu_num':stu_num,'user_count':user_count})
    elif request.method == "POST":
        id = request.POST.get("id")
        email = request.POST.get("email")
        password = request.POST.get("password")
        name = request.POST.get("name")
        group = request.POST.get("group")
        models.User.objects.create(user_id=id,email=email,tag=group,password=password,name=name)
        if group == '1':
            models.Teacher.objects.create(tea_id=id,email=email,name=name)
        elif group == '2':
            models.Student.objects.create(stu_id=id, email=email, name=name)
        return redirect("/index/manager")

def deluser(request):
    nid = request.GET.get("nid")
    models.User.objects.filter(user_id=nid).delete()
    if models.Teacher.objects.filter(tea_id=nid).exists():
        models.Teacher.objects.filter(tea_id=nid).delete()
    if models.Student.objects.filter(stu_id=nid).exists():
        models.Student.objects.filter(stu_id=nid).delete()
    return redirect("/index/manager")

def edituser(request,nid):
   if request.method == "GET":
       queryset = models.User.objects.all()
       user_count = models.Course.objects.all().count()
       man_num = 0
       tea_num = 0
       stu_num = 0
       for obj in queryset:
           if obj.tag == 0:
               man_num = man_num + 1
           elif obj.tag == 1:
               tea_num = tea_num + 1
           elif obj.tag == 2:
               stu_num = stu_num + 1
       row_object = models.User.objects.filter(user_id=nid).first()
       return render(request, 'edituser.html', {"row_object": row_object,'queryset': queryset,'man_num':man_num,'tea_num':tea_num,'stu_num':stu_num,'user_count':user_count})
   elif request.method == "POST":
       id = request.POST.get("id")
       email = request.POST.get("email")
       password = request.POST.get("password")
       name = request.POST.get("name")
       group = request.POST.get("group")
       models.User.objects.filter(user_id=nid).update(user_id=id,email=email,tag=group,password=password,name=name)
       if group == '1':
           models.Teacher.objects.filter(tea_id=nid).update(tea_id=id,email=email,name=name)
       elif group == '2':
           models.Student.objects.filter(stu_id=nid).update(stu_id=id, email=email, name=name)
       return redirect("/index/manager")

def addcourse(request):
    if request.method == "GET":
        queryset = models.User.objects.all()
        user_count = models.Course.objects.all().count()
        man_num = 0
        tea_num = 0
        stu_num = 0
        for obj in queryset:
            if obj.tag == 0:
                man_num = man_num + 1
            elif obj.tag == 1:
                tea_num = tea_num + 1
            elif obj.tag == 2:
                stu_num = stu_num + 1
        return render(request, "addcourse.html",
                      {'queryset': queryset, 'man_num': man_num, 'tea_num': tea_num, 'stu_num': stu_num,
                       'user_count': user_count})
    elif request.method == "POST":
        course_id = request.POST.get("course_id")
        course_name = request.POST.get("course_name")
        teacher_id = request.POST.get("teacher_id")
        credits = request.POST.get("credits")
        requirements = request.POST.get("requirements")
        models.Course.objects.create(
            course_id=course_id,
            course_name=course_name,
            teacher_id=teacher_id,
            credits=credits,
            requirements=requirements
        )
        return redirect("/index/manager/courseseek")

def courseseek(request):
    queryset = models.User.objects.all()
    course_count = models.Course.objects.all().count()
    man_num = 0
    tea_num = 0
    stu_num = 0
    for obj in queryset:
        if obj.tag == 0:
            man_num = man_num + 1
        elif obj.tag == 1:
            tea_num = tea_num + 1
        elif obj.tag == 2:
            stu_num = stu_num + 1
    course = models.Course.objects.all().order_by("course_id")
    return render(request, "course_seek.html",
                      {'course':course,'man_num': man_num, 'tea_num': tea_num, 'stu_num': stu_num,
                       'user_count':course_count})

def editcourse(request,nid):
   if request.method == "GET":
       queryset = models.User.objects.all()
       course_count = models.Course.objects.all().count()
       man_num = 0
       tea_num = 0
       stu_num = 0
       for obj in queryset:
           if obj.tag == 0:
               man_num = man_num + 1
           elif obj.tag == 1:
               tea_num = tea_num + 1
           elif obj.tag == 2:
               stu_num = stu_num + 1
       row_object = models.Course.objects.filter(course_id=nid).first()
       return render(request, 'editcourse.html', {"row_object": row_object,'queryset': queryset,'man_num':man_num,'tea_num':tea_num,'stu_num':stu_num,'course_count':course_count})
   elif request.method == "POST":
       course_id = request.POST.get("course_id")
       course_name = request.POST.get("course_name")
       teacher_id = request.POST.get("teacher_id")
       credits = request.POST.get("credits")
       requirements = request.POST.get("requirements")
       models.Course.objects.filter(course_id=course_id).update(
           course_id=course_id,
           course_name=course_name,
           teacher_id=teacher_id,
           credits=credits,
           requirements=requirements
       )
       return redirect("/index/manager/courseseek")

def delcourse(request):
    nid = request.GET.get("nid")
    models.Course.objects.filter(course_id=nid).delete()

    return redirect("/index/manager/courseseek")

def course_info(request,nid):
    queryset = models.User.objects.all()
    user_count = models.Course.objects.all().count()
    man_num = 0
    tea_num = 0
    stu_num = 0
    for obj in queryset:
        if obj.tag == 0:
            man_num = man_num + 1
        elif obj.tag == 1:
            tea_num = tea_num + 1
        elif obj.tag == 2:
            stu_num = stu_num + 1
    courseinfo = models.Course_info.objects.filter(course_id=nid).order_by("student_id").all()
    courseinfo_num = courseinfo.count()
    return render(request, "course_info.html",
                  {'queryset': queryset, 'man_num': man_num, 'tea_num': tea_num, 'stu_num': stu_num,
                   'user_count': user_count,"courseinfo":courseinfo,"courseinfo_num":courseinfo_num,"nid":nid})

def addcourse_info(request,nid):
    if request.method == "GET":
        queryset = models.User.objects.all()
        user_count = models.Course.objects.all().count()
        man_num = 0
        tea_num = 0
        stu_num = 0
        for obj in queryset:
            if obj.tag == 0:
                man_num = man_num + 1
            elif obj.tag == 1:
                tea_num = tea_num + 1
            elif obj.tag == 2:
                stu_num = stu_num + 1

        return render(request, "addcourseinfo.html",
                      {'queryset': queryset, 'man_num': man_num, 'tea_num': tea_num, 'stu_num': stu_num,
                       'user_count': user_count,"nid":nid})
    elif request.method == "POST":
        course_id = request.POST.get("course_id")
        student_id = request.POST.get("student_id")
        attend_point = request.POST.get("attend_point")
        exam_point = request.POST.get("exam_point")
        models.Course_info.objects.create(
            course_id=course_id,student_id=student_id,attend_point=attend_point,exam_point=exam_point
        )
        return redirect(f"/index/manager/{nid}/courseinfo")

def delcourse_info(request,nid):
    student_id = request.GET.get("student_id")
    models.Course_info.objects.filter(student_id=student_id,course_id=nid).delete()

    return redirect(f"/index/manager/{nid}/courseinfo")

def index_student(request):
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        query_condition = Q(course_id__contains=search_data) | Q(teacher_id__contains=search_data)
        data_dict['query_condition'] = query_condition
    else:
        # 如果 search_data 不存在，则默认查询条件为空
        data_dict['query_condition'] = Q()

    # 使用 get 方法获取 'query_condition' 键对应的值，如果不存在则为默认值 Q()
    query_condition = data_dict.get('query_condition')

    # 这里选择需要展示的字段，不使用 '__contains'
    queryset = models.Course.objects.filter(query_condition)
    infos = request.session.get('info')
    user_id = infos["user_id"]
    email = models.User.objects.filter(user_id=user_id).first().email
    password = models.User.objects.filter(user_id=user_id).first().password
    course_infos = models.Course_info.objects.filter(student_id=user_id)
    course_num = course_infos.count()
    unpass_num = 0
    yes_num = 0
    no_num = 0
    for obj in course_infos:
        if obj.attend_point and obj.exam_point:
            yes_num += 1
            if int(obj.attend_point) + int(obj.exam_point) <= 60:
                unpass_num += 1
        else:
            no_num += 1
    # 获取当前页码page，无指定的数即返回1
    page = int(request.GET.get('page', '1'))
    # 页码范围，一页多少个
    page_size = 10
    # 开始的页码和结束的页码
    start = (page - 1) * page_size
    end = page * page_size
    # queryset为当前页的数据
    queryset = models.Course_info.objects.filter(student_id=user_id).order_by("course_id")
    # 构建i一个新的链表
    fin_list = []
    for obj in queryset:
        # 寻找目的课程号和课程名
        dict_tem = {}
        tem1 = models.Course.objects.filter(course_id=obj.course_id).first()
        dict_tem[f"{tem1.course_id}"] = tem1.course_name
        # 寻找目的的教师id和姓名
        tem2 = models.Teacher.objects.filter(tea_id=tem1.teacher_id).first()
        dict_tem[f"{tem2.tea_id}"] = tem2.name
        dict_tem["credits"] = tem1.credits
        dict_tem["requirements"] = tem1.requirements
        if obj.attend_point and obj.exam_point:
            score = int(obj.attend_point) + int(obj.exam_point)
            dict_tem["score"] = str(score)
        else:
            dict_tem["score"] = ""
        fin_list.append(dict_tem)
    # 总的条数
    total_count = models.Course_info.objects.filter(student_id=user_id).count()
    # 获取要分多少个页以及页尾有多少个条数
    total_page_count, div = divmod(total_count, page_size)
    # 如果页尾为空的话，页数+1
    if div:
        total_page_count += 1
    # 前端页面中可见的页数
    visible_pages = 5
    if total_page_count <= visible_pages * 2 + 1:
        start_page = 1
        end_page = total_page_count
    else:
        if page <= visible_pages:
            start_page = 1
            end_page = page + visible_pages
        elif page >= total_page_count - visible_pages:
            start_page = page - visible_pages
            end_page = total_page_count
        else:
            start_page = page - visible_pages
            end_page = page + visible_pages

    # 设置一个空列表，用在前端写对应的页码
    page_str_list = []
    ele = '<li class="page-item"><a class="page-link" href="?page={}">首页</a></li>'.format(1)
    page_str_list.append(ele)
    if page > 1:
        ele = '<li class="page-item"><a class="page-link" href="?page={}">上一页</a></li>'.format(page - 1)
        page_str_list.append(ele)
    for i in range(start_page, end_page + 1):
        if i == page:
            ele = '<li class="page-item active"><a class="page-link" href="?page={}">{}</a></li>'.format(i, i)
        else:
            ele = '<li class="page-item"><a class="page-link" href="?page={}">{}</a></li>'.format(i, i)
        page_str_list.append(ele)
    if page < total_page_count:
        ele = '<li class="page-item"><a class="page-link" href="?page={}">下一页</a></li>'.format(page + 1)
        page_str_list.append(ele)
    ele = '<li class="page-item"><a class="page-link" href="?page={}">尾页</a></li>'.format(total_page_count)
    page_str_list.append(ele)
    page_string = mark_safe("".join(page_str_list))
    return render(request, "index_student.html",
                  {'queryset': queryset, 'course_num': course_num, 'unpass_num': unpass_num, 'yes_num': yes_num,
                   'no_num': no_num, "search_data": search_data, "page_string": page_string, "fin_list": fin_list,
                   "password": password, "email": email})

def stu_email(request):
    infos = request.session.get('info')
    user_id = infos["user_id"]
    email = models.User.objects.filter(user_id=user_id).first().email
    password = models.User.objects.filter(user_id=user_id).first().password
    form = ChangeEmailForm()
    if request.method == "GET":
        course_infos = models.Course_info.objects.filter(student_id=user_id)
        course_num = course_infos.count()
        unpass_num = 0
        yes_num = 0
        no_num = 0
        for obj in course_infos:
            if obj.attend_point and obj.exam_point:
                yes_num += 1
                if int(obj.attend_point) + int(obj.exam_point) <= 60:
                    unpass_num += 1
            else:
                no_num += 1
        old_email = models.User.objects.filter(user_id=user_id).first().email
        return render(request, "stu_email.html",
                      {'course_num': course_num, 'unpass_num': unpass_num, 'yes_num': yes_num,
                       'no_num': no_num,"old_email":old_email,"form":form,"password":password,"email":email})
    elif request.method == "POST":
        infos = request.POST.get("new_email")
        models.User.objects.filter(user_id=user_id).update(email=infos)
        models.Student.objects.filter(stu_id=user_id).update(email=infos)
        return redirect("/index/student")

def stu_password(request):
    infos = request.session.get('info')
    user_id = infos["user_id"]
    email = models.User.objects.filter(user_id=user_id).first().email
    password = models.User.objects.filter(user_id=user_id).first().password
    form = ChangePasswordForm()
    if request.method == "GET":
        course_infos = models.Course_info.objects.filter(student_id=user_id)
        course_num = course_infos.count()
        unpass_num = 0
        yes_num = 0
        no_num = 0
        for obj in course_infos:
            if obj.attend_point and obj.exam_point:
                yes_num += 1
                if int(obj.attend_point) + int(obj.exam_point) <= 60:
                    unpass_num += 1
            else:
                no_num += 1
        old_email = models.User.objects.filter(user_id=user_id).first().email
        return render(request, "stu_password.html",
                      {'course_num': course_num, 'unpass_num': unpass_num, 'yes_num': yes_num,
                       'no_num': no_num, "old_email": old_email, "form": form, "password": password, "email": email})
    elif request.method == "POST":
        infos = request.POST.get("new_password")
        models.User.objects.filter(user_id=user_id).update(password=infos)
        return redirect("/index/student")

def index_teacher(request):
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        query_condition = Q(course_id__contains=search_data) | Q(credits__contains=search_data)
        data_dict['query_condition'] = query_condition
    else:
        # 如果 search_data 不存在，则默认查询条件为空
        data_dict['query_condition'] = Q()

    # 使用 get 方法获取 'query_condition' 键对应的值，如果不存在则为默认值 Q()
    query_condition = data_dict.get('query_condition')

    # 这里选择需要展示的字段，不使用 '__contains'
    queryset = models.Course.objects.filter(query_condition)
    infos = request.session.get('info')
    user_id = infos["user_id"]
    email = models.User.objects.filter(user_id=user_id).first().email
    password = models.User.objects.filter(user_id=user_id).first().password
    infos = models.Course.objects.filter(teacher_id=user_id)
    course_num = infos.count()
    stu_num = 0
    yes_num = 0
    no_num = 0
    for obj in infos:
        infos2 = models.Course_info.objects.filter(course_id=obj.course_id)
        stu_num += infos2.count()
        for obj2 in infos2:
            if obj2.attend_point and obj2.exam_point:
                yes_num += 1
            else:
                no_num += 1

    # 获取当前页码page，无指定的数即返回1
    page = int(request.GET.get('page', '1'))
    # 页码范围，一页多少个
    page_size = 10
    # 开始的页码和结束的页码
    start = (page - 1) * page_size
    end = page * page_size
    # queryset为当前页的数据
    queryset = models.Course.objects.filter(teacher_id=user_id).order_by("course_id")
    total_count = models.Course.objects.filter(teacher_id=user_id).count()
    # 获取要分多少个页以及页尾有多少个条数
    total_page_count, div = divmod(total_count, page_size)
    # 如果页尾为空的话，页数+1
    if div:
        total_page_count += 1
    # 前端页面中可见的页数
    visible_pages = 5
    if total_page_count <= visible_pages * 2 + 1:
        start_page = 1
        end_page = total_page_count
    else:
        if page <= visible_pages:
            start_page = 1
            end_page = page + visible_pages
        elif page >= total_page_count - visible_pages:
            start_page = page - visible_pages
            end_page = total_page_count
        else:
            start_page = page - visible_pages
            end_page = page + visible_pages

    # 设置一个空列表，用在前端写对应的页码
    page_str_list = []
    ele = '<li class="page-item"><a class="page-link" href="?page={}">首页</a></li>'.format(1)
    page_str_list.append(ele)
    if page > 1:
        ele = '<li class="page-item"><a class="page-link" href="?page={}">上一页</a></li>'.format(page - 1)
        page_str_list.append(ele)
    for i in range(start_page, end_page + 1):
        if i == page:
            ele = '<li class="page-item active"><a class="page-link" href="?page={}">{}</a></li>'.format(i, i)
        else:
            ele = '<li class="page-item"><a class="page-link" href="?page={}">{}</a></li>'.format(i, i)
        page_str_list.append(ele)
    if page < total_page_count:
        ele = '<li class="page-item"><a class="page-link" href="?page={}">下一页</a></li>'.format(page + 1)
        page_str_list.append(ele)
    ele = '<li class="page-item"><a class="page-link" href="?page={}">尾页</a></li>'.format(total_page_count)
    page_str_list.append(ele)
    page_string = mark_safe("".join(page_str_list))
    return render(request, "index_teacher.html",
                  {'queryset': queryset, 'course_num': course_num, 'stu_num': stu_num, 'yes_num': yes_num,
                   'no_num': no_num, "search_data": search_data, "page_string": page_string, "password": password,
                   "email": email})

def tea_email(request):
    infos = request.session.get('info')
    user_id = infos["user_id"]
    email = models.User.objects.filter(user_id=user_id).first().email
    password = models.User.objects.filter(user_id=user_id).first().password
    form = ChangeEmailForm()
    if request.method == "GET":
        email = models.User.objects.filter(user_id=user_id).first().email
        password = models.User.objects.filter(user_id=user_id).first().password
        infos = models.Course.objects.filter(teacher_id=user_id)
        course_num = infos.count()
        stu_num = 0
        yes_num = 0
        no_num = 0
        for obj in infos:
            infos2 = models.Course_info.objects.filter(course_id=obj.course_id)
            stu_num += infos.count()
            for obj2 in infos2:
                if obj2.attend_point and obj2.exam_point:
                    yes_num += 1
                else:
                    no_num += 1
        return render(request, "tea_email.html",
                      {'course_num': course_num, 'stu_num': stu_num,  'yes_num': yes_num,
                       'no_num': no_num, "form": form, "password": password, "email": email})
    elif request.method == "POST":
        infos = request.POST.get("new_email")
        models.User.objects.filter(user_id=user_id).update(email=infos)
        models.Teacher.objects.filter(tea_id=user_id).update(email=infos)
        return redirect("/index/teacher")

def editpoint(request,nid):
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        query_condition = Q(student_id__contains=search_data) | Q(attend_point__contains=search_data) | Q(exam_point__contains=search_data)
        data_dict['query_condition'] = query_condition
    else:
        # 如果 search_data 不存在，则默认查询条件为空
        data_dict['query_condition'] = Q()

    # 使用 get 方法获取 'query_condition' 键对应的值，如果不存在则为默认值 Q()
    query_condition = data_dict.get('query_condition')

    # 这里选择需要展示的字段，不使用 '__contains'
    queryset = models.Course_info.objects.filter(query_condition)
    infos = request.session.get('info')
    user_id = infos["user_id"]
    email = models.User.objects.filter(user_id=user_id).first().email
    password = models.User.objects.filter(user_id=user_id).first().password
    infos = models.Course.objects.filter(teacher_id=user_id)
    course_num = infos.count()
    stu_num = 0
    yes_num = 0
    no_num = 0
    for obj in infos:
        infos2 = models.Course_info.objects.filter(course_id=obj.course_id)
        stu_num += infos2.count()
        for obj2 in infos2:
            if obj2.attend_point and obj2.exam_point:
                yes_num += 1
            else:
                no_num += 1

    # 获取当前页码page，无指定的数即返回1
    page = int(request.GET.get('page', '1'))
    # 页码范围，一页多少个
    page_size = 10
    # 开始的页码和结束的页码
    start = (page - 1) * page_size
    end = page * page_size
    # queryset为当前页的数据
    queryset = models.Course_info.objects.filter(course_id=nid).order_by("student_id")
    total_count = queryset.count()
    fin_list = []
    for obj in queryset:
        tem_list = []
        tem_list.append(obj.student_id)
        tem_list.append(models.Student.objects.filter(stu_id=obj.student_id).first().name)
        tem_list.append(obj.attend_point)
        tem_list.append(obj.exam_point)
        fin_list.append(tem_list)

    total_page_count, div = divmod(total_count, page_size)
    # 如果页尾为空的话，页数+1
    if div:
        total_page_count += 1
    # 前端页面中可见的页数
    visible_pages = 5
    if total_page_count <= visible_pages * 2 + 1:
        start_page = 1
        end_page = total_page_count
    else:
        if page <= visible_pages:
            start_page = 1
            end_page = page + visible_pages
        elif page >= total_page_count - visible_pages:
            start_page = page - visible_pages
            end_page = total_page_count
        else:
            start_page = page - visible_pages
            end_page = page + visible_pages

    # 设置一个空列表，用在前端写对应的页码
    page_str_list = []
    ele = '<li class="page-item"><a class="page-link" href="?page={}">首页</a></li>'.format(1)
    page_str_list.append(ele)
    if page > 1:
        ele = '<li class="page-item"><a class="page-link" href="?page={}">上一页</a></li>'.format(page - 1)
        page_str_list.append(ele)
    for i in range(start_page, end_page + 1):
        if i == page:
            ele = '<li class="page-item active"><a class="page-link" href="?page={}">{}</a></li>'.format(i, i)
        else:
            ele = '<li class="page-item"><a class="page-link" href="?page={}">{}</a></li>'.format(i, i)
        page_str_list.append(ele)
    if page < total_page_count:
        ele = '<li class="page-item"><a class="page-link" href="?page={}">下一页</a></li>'.format(page + 1)
        page_str_list.append(ele)
    ele = '<li class="page-item"><a class="page-link" href="?page={}">尾页</a></li>'.format(total_page_count)
    page_str_list.append(ele)
    page_string = mark_safe("".join(page_str_list))
    return render(request, "edit_point.html",
                  {'fin_list':fin_list, 'course_num': course_num, 'stu_num': stu_num, 'yes_num': yes_num,
                   'no_num': no_num, "search_data": search_data, "page_string": page_string, "password": password,
                   "email": email})

def tea_password(request):
    infos = request.session.get('info')
    user_id = infos["user_id"]
    email = models.User.objects.filter(user_id=user_id).first().email
    password = models.User.objects.filter(user_id=user_id).first().password
    form = ChangePasswordForm()
    if request.method == "GET":
        email = models.User.objects.filter(user_id=user_id).first().email
        password = models.User.objects.filter(user_id=user_id).first().password
        infos = models.Course.objects.filter(teacher_id=user_id)
        course_num = infos.count()
        stu_num = 0
        yes_num = 0
        no_num = 0
        for obj in infos:
            infos2 = models.Course_info.objects.filter(course_id=obj.course_id)
            stu_num += infos.count()
            for obj2 in infos2:
                if obj2.attend_point and obj2.exam_point:
                    yes_num += 1
                else:
                    no_num += 1
        return render(request, "tea_password.html",
                      {'course_num': course_num, 'stu_num': stu_num, 'yes_num': yes_num,
                       'no_num': no_num,"form": form, "password": password, "email": email})
    elif request.method == "POST":
        infos = request.POST.get("new_password")
        models.User.objects.filter(user_id=user_id).update(password=infos)
        return redirect("/index/teacher")
def tables(re):
    return render(re,"tables.html")

def index(re):
    return render(re,"index.html")
def forms(re):
    return render(re,"forms.html")