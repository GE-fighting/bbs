from django.contrib import auth
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from blog import forms, models
from geetest import GeetestLib
from django.db.models import Count

from untils import zhenzismsclient as smsclient
from untils.testRedis import saveCode,record_up,get_top_n_articles
import random


def sendCode(request):
    phone = request.GET.get("phone")
    strCode = ""  ##生成6位随机验证码
    for i in range(0, 6):
        strCode = strCode + str(random.randint(0, 9))
    client = smsclient.ZhenziSmsClient("https://sms_developer.zhenzikj.com", "105034",
                                           "2a6ef5e2-aa69-408a-b03d-be9ca79e8010")
    params = {'message': '您的验证码为:' + strCode, 'number': phone}
    result = client.send(params)
    saveCode(phone, strCode)
    result = {"code": 0}
    return JsonResponse(result, safe=False)


# Create your views here.

# 自定义分页（Bootstrap版）
class Pagination(object):
    """自定义分页（Bootstrap版）"""
    def __init__(self, current_page, total_count, base_url, per_page=5, max_show=11):
        """
        :param current_page: 当前请求的页码
        :param total_count: 总数据量
        :param base_url: 请求的URL
        :param per_page: 每页显示的数据量，默认值为10
        :param max_show: 页面上最多显示多少个页码，默认值为11
        """
        try:
            self.current_page = int(current_page)
        except Exception as e:
            # 取不到或者页码数不是数字都默认展示第1页
            self.current_page = 1
        # 定义每页显示多少条数据
        self.per_page = per_page
        # 计算出总页码数
        total_page, more = divmod(total_count, per_page)
        if more:
            total_page += 1
        self.total_page = total_page
        # 定义页面上最多显示多少页码(为了左右对称，一般设为奇数)
        self.max_show = max_show
        self.half_show = max_show // 2
        self.base_url = base_url

    @property
    def start(self):
        return (self.current_page - 1) * self.per_page

    @property
    def end(self):
        return self.current_page * self.per_page

    def page_html(self):
        # 计算一下页面显示的页码范围
        if self.total_page <= self.max_show:  # 总页码数小于最大显示页码数
            page_start = 1
            page_end = self.total_page
        elif self.current_page + self.half_show >= self.total_page:  # 右边越界
            page_end = self.total_page
            page_start = self.total_page - self.max_show
        elif self.current_page - self.half_show <= 1:  # 左边越界
            page_start = 1
            page_end = self.max_show
        else:  # 正常页码区间
            page_start = self.current_page - self.half_show
            page_end = self.current_page + self.half_show
        # 生成页面上显示的页码
        page_html_list = []
        page_html_list.append('<nav aria-label="Page navigation"><ul class="pagination">')
        # 加首页
        first_li = '<li><a href="{}?page=1">首页</a></li>'.format(self.base_url)
        page_html_list.append(first_li)
        # 加上一页
        if self.current_page == 1:
            prev_li = '<li><a href="#"><span aria-hidden="true">&laquo;</span></a></li>'
        else:
            prev_li = '<li><a href="{}?page={}"><span aria-hidden="true">&laquo;</span></a></li>'.format(
                self.base_url, self.current_page - 1)
        page_html_list.append(prev_li)
        for i in range(page_start, page_end + 1):
            if i == self.current_page:
                li_tag = '<li class="active"><a href="{0}?page={1}">{1}</a></li>'.format(self.base_url, i)
            else:
                li_tag = '<li><a href="{0}?page={1}">{1}</a></li>'.format(self.base_url, i)
            page_html_list.append(li_tag)
        # 加下一页
        if self.current_page == self.total_page:
            next_li = '<li><a href="#"><span aria-hidden="true">&raquo;</span></a></li>'
        else:
            next_li = '<li><a href="{}?page={}"><span aria-hidden="true">&raquo;</span></a></li>'.format(
                self.base_url, self.current_page + 1)
        page_html_list.append(next_li)
        # 加尾页
        page_end_li = '<li><a href="{}?page={}">尾页</a></li>'.format(self.base_url, self.total_page)
        page_html_list.append(page_end_li)
        page_html_list.append('</ul></nav>')
        return "".join(page_html_list)


# 请在官网申请ID使用，示例ID不可使用
pc_geetest_id = "b46d1900d0a894591916ea94ea91bd2c"
pc_geetest_key = "36fc3fe98530eea08dfc6ce76e3d24c4"


# 登录视图函数
def login(request):
    if request.method == "POST":
        ret = {"status": 0, "msg": ""}  # 初始化一个给AJAX返回的数据
        username = request.POST.get("username")
        password = request.POST.get("password")
        # 获取极验，滑动验证码相关参数
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.POST.get(gt.FN_CHALLENGE, '')
        validate = request.POST.get(gt.FN_VALIDATE, '')
        seccode = request.POST.get(gt.FN_SECCODE, '')
        status = request.session[gt.GT_STATUS_SESSION_KEY]
        user_id = request.session["user_id"]
        if status:
            result = gt.success_validate(challenge, validate, seccode, user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)
        if result:
            # 验证码正确
            # 利用auth模块做用户名和密码的校验
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)  # 将登陆用户注入request.user
                ret["msg"] = "/index/"
            else:
                # 用户名密码错误
                ret["status"] = 1
                ret["msg"] = "用户名或密码错误！"
        else:
            ret["status"] = 2
            ret["msg"] = "验证码错误"
        return JsonResponse(ret)
    return render(request, "login.html")


# 获得极验。滑动验证码视图函数
def get_geetest(request):
    user_id = 'test'
    gt = GeetestLib(pc_geetest_id, pc_geetest_key)
    status = gt.pre_process(user_id)
    request.session[gt.GT_STATUS_SESSION_KEY] = status
    request.session["user_id"] = user_id
    response_str = gt.get_response_str()
    return HttpResponse(response_str)


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

#主页面视图函数
def index(request):
    # 从URL中取当前访问的页码数
    # current_page = int(request.GET.get('page'))
    # 比len(models.Publisher.objects.all())更高效
    current_page = 1
    value = request.GET.get('page')
    if value:
        current_page = int(value)
    total_count = models.Article.objects.count()
    page_obj = Pagination(current_page, total_count, request.path_info)
    data = models.Article.objects.all()[page_obj.start:page_obj.end]
    page_html = page_obj.page_html()
    top10 = get_top_n_articles(10)
    print("-------------------------------------")
    print(top10)
    return render(request, "index.html", {"article_list": data, "article_top":top10,"page_html": page_html})


# 注册的视图函数
def register(request):
    if request.method == "POST":
        ret = {"status": 0, "msg": ""}
        forms_obj = forms.RegForm(request.POST)
        # 帮我做校验
        if forms_obj.is_valid():
            # 校验通过，去数据库创建一个用户
            forms_obj.cleaned_data.pop("re_password")
            forms_obj.cleaned_data.pop("code")
            avatar_img = request.FILES.get("avatar")  # 得到头像文件
            if avatar_img == None:
                avatar_img = "avatars/default.jpg"
            models.UserInfo.objects.create_user(**forms_obj.cleaned_data, avatar=avatar_img)
            user = auth.authenticate(
                username=forms_obj.cleaned_data["username"],
                password=forms_obj.cleaned_data["password"])
            auth.login(request, user)
            ret["msg"] = "/index/"
            return JsonResponse(ret)
        else:
            # print(forms_obj.errors)
            ret["status"] = 1
            ret["msg"] = forms_obj.errors
            return JsonResponse(ret)
    # 生成一个form对象
    form_obj = forms.RegForm()
    return render(request, "register.html", {"form_obj": form_obj})


# 注销的视图函数
def logout(request):
    auth.logout(request)
    return redirect("/index/")


# ----------------个人博客站点视图函数------------------#

# 获取全部文章
def home(request, username):
    user = models.UserInfo.objects.filter(username=username).first()
    if not user:
        return render(request,"404.html")
    blog = user.blog
    print("从主页面走")
    # 我的文章列表
    article_list = models.Article.objects.filter(user=user)
    #     # 我的文章分类和分类下的文章数
    category_list, archive_list, tag_list, concerned_users = get_left_menu(username)
    return render(request, "home.html", {
        "blog": blog,
        "username": username,
        "article_list": article_list,
        "category_list": category_list,
        "archive_list": archive_list,
        "tag_list": tag_list,
        "concerned_users":concerned_users
    })


# 获取该分类下的文章
def home_category(request, username, category_title):
    user = models.UserInfo.objects.filter(username=username).first()
    if not user:
        return render(request, "404.html")
    blog = user.blog
    category = models.Category.objects.filter(blog=blog, title=category_title)
    article_list = models.Article.objects.filter(user=user, category=category)
    print(article_list)
    category_list, archive_list, tag_list,concerned_users = get_left_menu(username)
    return render(request, "home.html", {
        "blog": blog,
        "username": username,
        "article_list": article_list,
        "category_list": category_list,
        "archive_list": archive_list,
        "tag_list": tag_list,
        "concerned_users":concerned_users
    })


# 获取该标签下的文章
def home_tag(request, username, tag_title):
    user = models.UserInfo.objects.filter(username=username).first()
    if not user:
        return render(request,"404.html")
    blog = user.blog
    tag = models.Tag.objects.filter(blog=blog, title=tag_title)
    articletotag_list = list(models.ArticleToTag.objects.filter(tag=tag))
    article_list = []
    for articletotag in articletotag_list:
        article_list.append(articletotag.article)
    category_list, archive_list, tag_list,concerned_users = get_left_menu(username)
    return render(request, "home.html", {
        "blog": blog,
        "username": username,
        "article_list": article_list,
        "category_list": category_list,
        "archive_list": archive_list,
        "tag_list": tag_list,
        "concerned_users":concerned_users
    })


# 获取该时间归档下的文章
def home_archive(request, username, time):
    user = models.UserInfo.objects.filter(username=username).first()
    if not user:
        return render(request,"404.html")
    blog = user.blog
    article_default_list = list(models.Article.objects.filter(user=user))
    article_list = []
    for article in article_default_list:
        if article.create_time.strftime("%Y-%m") == time:
            article_list.append(article)
    category_list, archive_list, tag_list,concerned_users = get_left_menu(username)
    return render(request, "home.html", {
        "blog": blog,
        "username": username,
        "article_list": article_list,
        "category_list": category_list,
        "archive_list": archive_list,
        "tag_list": tag_list,
        "concerned_users":concerned_users
    })


# ----------------!个人博客站点视图函数------------------#

# 获得左侧视图菜单数据的视图函数
def get_left_menu(username):
    user = models.UserInfo.objects.filter(username=username).first()
    blog = user.blog
    # 我的文章分类和分类下的文章数
    category_list = models.Category.objects.filter(blog=blog)  # 我的文章分类
    # 我的文章标签和标签下的文章数，与上面的文章分类方法不同，但原理类似
    tag_list = models.Tag.objects.filter(blog=blog).annotate(c=Count("article")).values("title", "c")

    # 按日期归档
    archive_list = models.Article.objects.filter(user=user).extra(
        select={"archive_ym": "date_format(create_time,'%%Y-%%m')"}
    ).values("archive_ym").annotate(c=Count("nid")).values("archive_ym", "c")
    #关注的人
    concerned_users = models.UserConcern.objects.filter(concern=user)
    return category_list, archive_list, tag_list,concerned_users


# 获取文章内容的视图函数
def article_detail(request, username, pk):
    '''
    :param:username:被访问的blog的用户名
    :param request:
    :param pk:访问文章的主键
    :return:
    '''
    user = models.UserInfo.objects.filter(username=username).first()
    if not user:
        return render(request,"404.html")
    blog = user.blog
    article_obj = models.Article.objects.filter(pk=pk).first()  # 用first()装换成Article对象，不然是Query set 对象
    category_list, archive_list, tag_list = get_left_menu(username)
    comment_list = models.Comments.objects.filter(article_id=pk)
    print(comment_list)
    return render(request,
                  'article_detail.html',
                  {"article": article_obj,
                   "blog": blog,
                   "username": username,
                   "category_list": category_list,
                   "archive_list": archive_list,
                   "tag_list": tag_list,
                   "comment_list": comment_list
                   })


import json
from django.db.models import F


# 点赞功能视图函数
def up_down(request):
    ret = {"status": True, "msg_is_up": ""}  # 返回给ajax的字典
    is_up = json.loads(request.POST.get("is_up"))#把Js语法的boolen值转化为pyhon的boolen值
    article_id = request.POST.get("article_id")#获取前台传的文章id值
    user = request.user    #获取用户对象
    try:
        models.ArticleUpDown.objects.create(user=user, article_id=article_id, is_up=is_up)#尝试在文章点赞表里添加一条记录
        if is_up:   #如果是点赞，则让该文章点赞数加一
            record_up(article_id, 5)
            print("redis错误")
            models.Article.objects.filter(pk=article_id).update(up_count=F("up_count") + 1)
             #在redis增加该篇文章的点赞数
        else:       #如果是踩，则让文章踩数加一
            models.Article.objects.filter(pk=article_id).update(down_count=F("down_count") + 1)
    except Exception as e:#如果在文章添加表里创建记录失败，则查看该用户对该片文章已有的点赞情况
        msg_is_up = models.ArticleUpDown.objects.filter(user=user, article_id=article_id).first().is_up
        ret["status"] = False #将创建记录（点赞或踩是否成功）设为false,及不成功
        ret["msg_is_up"] = msg_is_up #将该用户对该文章的态度赋值，便于在前端查看
    return JsonResponse(ret)                #返回状态集





# 获取评论列表视图函数
def comment(requets):
    ret = {}
    user_id = requets.user.pk
    comment = requets.POST.get("comment")
    article_id = requets.POST.get("article_id")
    pid = requets.POST.get("pid")
    if not pid:
        comment_obj = models.Comments.objects.create(user_id=user_id, article_id=article_id, content=comment)
    else:
        comment_obj = models.Comments.objects.create(user_id=user_id, article_id=article_id, content=comment,
                                                     parent_comment_id=pid)
    ret["create_time"] = comment_obj.create_time.strftime("%Y-%m-%d")
    ret["username"] = comment_obj.user.username
    ret["content"] = comment_obj.content
    return JsonResponse(ret)


#####################文章管理功能##############

from bs4 import BeautifulSoup


# 添加文章
def add_article(request):
    blog = request.user.blog
    category_list = models.Category.objects.filter(blog=blog)
    tag_list = models.Tag.objects.filter(blog=blog)
    if request.method == 'POST':
        title = request.POST.get("title")
        content = request.POST.get("content")
        category_id = request.POST.get("category")  # get方法即可获取radio的值
        tagId_list = request.REQUEST.getlist("tag")  # getlist方法获取checkbox值
        soup = BeautifulSoup(content, "html.parser")
        desc = soup.text[0:150] + '...'
        user = request.user
        # 防止xss攻击，删除非法标签
        for tag in soup.find_all():
            print(tag.name)
            if tag.name in ["script", "link"]:
                tag.decompose()
        try:
            article_obj = models.Article.objects.create(title=title, desc=desc, user=user, category_id=category_id)
            models.ArticleDetail.objects.create(content=str(soup), article=article_obj)
            print(type(article_obj))
            for tagId in tag_list:
                print(type(tagId))
                # article_obj.tags.add(tagId)
                # article_obj.save()
                models.ArticleToTag.objects.create(article=article_obj, tag=tagId)
            return render(request, "backend/article_success.html", {"article": article_obj})
        except Exception as e:
            return render(request, "backend/add_article.html", {"result": 0})
    return render(request, "backend/add_article.html", {"category_list": category_list, "tag_list": tag_list})


# 返回文章列表
def article_list(request):
    user = request.user
    article_list = models.Article.objects.filter(user=user)
    return render(request, "backend/article_list.html", {"article_list": article_list})


# 删除文章
def article_delete(request):
    ret = {"status": 1, "msg": ""}
    article_id = request.GET.get("id")
    try:
        models.Article.objects.filter(pk=article_id).delete()
        models.ArticleUpDown.objects.filter(article_id=article_id).delete() #在文章点赞表里查找该文章记录，全部删除
    except Exception as e:
        ret["status"] = 0
    return JsonResponse(ret)


def article_edit(request):
    blog = request.user.blog
    category_list = models.Category.objects.filter(blog=blog)
    id = request.GET.get("id")
    category_id = models.Article.objects.filter(pk=id).first().category
    article_detail_obj = models.ArticleDetail.objects.filter(article_id=id).first()
    return render(request, "backend/article_edit.html",
                  {"article_detail_obj": article_detail_obj,
                   "category_list": category_list,
                   "category_id": category_id}
                  )


#####################！文章管理功能##############

# -------------------博客管理页面视图-----------------#
def blog_manage(requets):
    if requets.method == "POST":
        msg = {"status": 1, "info": ""}
        title = requets.POST.get("title")
        site = requets.POST.get("site")
        style = requets.POST.get("style")
        print(title, site, style)
        try:
            blog_obj = models.Blog.objects.create(title=title, site=site, theme=style)
            user_obj = models.UserInfo.objects.filter(username=requets.user.username).first()
            user_obj.blog = blog_obj
            user_obj.save()
            msg["info"] = "博客已成功创建"
        except Exception as e:
            print(e)
            msg["status"] = 0
            msg["info"] = "博客创建失败"
        return JsonResponse(msg)
    return render(requets, "backend/blog_manage.html")


# -------------------!博客管理页面视图-----------------#

# --------------------分类管理视图函数------------------#

def classify_manage(request):
    blog_pk = request.user.blog.pk
    classify_list = models.Category.objects.filter(blog_id=blog_pk)
    print(type(classify_list))
    return render(request, "backend/classify_manage.html", {"classify_list": classify_list})


def delClassify(request):
    ret = {"status": 1}
    pk = request.GET.get("id")
    models.Category.objects.filter(nid=pk).delete()
    return JsonResponse(ret)


def addClassify(request):
    msg = {"status": 1}
    title = request.POST.get("title")
    blog_pk = request.user.blog.pk
    try:
        models.Category.objects.create(title=title, blog_id=blog_pk)
    except Exception as e:
        print(e)
        msg["status"] = 0
    return JsonResponse(msg)


def editCategory(request):
    ret = {"status": 1, "msg": ""}
    title = request.GET.get("title")
    id = request.GET.get("id")
    try:
        models.Category.objects.filter(pk=id).update(title=title)
        ret["msg"] = "修改成功"
    except Exception as e:
        print(e)
        ret["status"] = 0
        ret["msg"] = e
    return JsonResponse(ret)


# ---------------------!分类管理视图函数------------------------#

# ---------------------标签管理视图函数------------------------#
# 返回所有的标签
def tag_list(request):
    blog = request.user.blog
    tag_list = models.Tag.objects.filter(blog=blog)
    return render(request, "backend/tag_list.html", {"tag_list": tag_list})


# 新增标签
def addTag(request):
    msg = {"status": 1}
    title = request.POST.get("title")
    blog_pk = request.user.blog.pk
    try:
        models.Tag.objects.create(title=title, blog_id=blog_pk)
    except Exception as e:
        print(e)
        msg["status"] = 0
    return JsonResponse(msg)


# 删除标签
def delTag(request):
    ret = {"status": 1}
    pk = request.GET.get("id")
    models.Tag.objects.filter(nid=pk).delete()
    return JsonResponse(ret)


# 修改标签
def editTag(request):
    ret = {"status": 1, "msg": ""}
    title = request.GET.get("title")
    id = request.GET.get("id")
    try:
        models.Tag.objects.filter(pk=id).update(title=title)
        ret["msg"] = "修改成功"
    except Exception as e:
        print(e)
        ret["status"] = 0
        ret["msg"] = e
    return JsonResponse(ret)


# ---------------------！标签管理视图函数------------------------#


#----------------------用户中心管理视图-------------------------#



#----------------------！用户中心管理视图-------------------------#

from bbs import settings
import os


# 富本编辑器上传图片
def upload(request):
    print(request.FILES)
    obj = request.FILES.get("uploadImg")
    path = os.path.join(settings.MEDIA_ROOT, "add_article_img", obj.name)
    with open(path, "wb") as f:
        for line in obj:
            f.write(line)
    ret = {
        "error": 0,
        "url": "/media/add_article_img/" + obj.name
    }
    return JsonResponse(ret)
