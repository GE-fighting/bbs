from django.conf.urls import url
from blog import views

urlpatterns = [
    url(r"up_down/", views.up_down),
    url(r'comment/', views.comment),

    # ------------关注功能------------#
    url(r'addConcern/', views.addConcern),  # 添加关注用户
    url(r'cancelConcern/', views.cancelConcern),  # 添加关注用户
    # ------------!关注功能------------#

    #--------------个人中心管理-----------#
    url(r'backend/userManager/', views.userManager),
    url(r'backend/userManager/edit_profile/', views.userManager),
    #--------------！个人中心管理-----------#

    ###########文章管理url################
    url(r'backend/add_article/', views.add_article),
    url(r'backend/article_list/', views.article_list),
    url(r'backend/article_delete/', views.article_delete),
    url(r'backend/article_edit/', views.article_edit),
    ###########!文章管理url################

    ############博客管理#############
    url(r'backend/blog_manage/', views.blog_manage),  # 博客管理
    ############博客管理#############

    ############分类管理############
    url(r'backend/classify_manage/', views.classify_manage),  # 文章分类管理
    url(r'backend/edit_category/', views.editCategory),  # 文章修改分类
    ############分类管理#############

    ############标签管理###########
    url(r'backend/tag_list/', views.tag_list),  # 文章分类管理
    url(r'backend/addTag/', views.addTag),  # 文章分类管理
    url(r'backend/delTag/', views.delTag),  # 文章分类管理
    url(r'backend/edit_tag/', views.editTag),  # 文章修改分类
    ########个人站点############
    url(r'(\w+)/article/(\d+)/$', views.article_detail),  # 文章详情
    url(r'(\w+)/category/(\w+)/$', views.home_category),
    url(r'(\w+)/tag/(.+)/$', views.home_tag),  # home_tag(request,username.tag_title)
    url(r'(\w+)/archive/(.+)/$', views.home_archive),  # home_tag(request,username.tag_title)
    url(r'(\w+)/', views.home),  # home(request,username)进入个人站点
    ########个人站点############

]
