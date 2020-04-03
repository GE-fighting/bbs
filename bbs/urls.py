from django.conf.urls import include, url
from django.contrib import admin
from django.views.static import serve
from blog import urls as blog_urls
from blog import views
from django.conf import settings
urlpatterns = [
    # Examples:
    # url(r'^$', 'bbs.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^sendCode/', views.sendCode),
    url(r'^pc-geetest/register', views.get_geetest),
    url(r'^login/', views.login),
    url(r'^reg/', views.register),
    url(r'^index/', views.index),
    url(r'^logout/', views.logout),
    url(r'^upload/', views.upload),
    url(r'^addClassify/', views.addClassify),
    url(r'^delClassify/', views.delClassify),
    # media的相关路由配置
    url(r'^media/(?P<path>.*)$', serve, {"document_root":settings.MEDIA_ROOT}),
    #将所有以blog开头的url都教给app下面的urls处理
    url(r"^blog/",include(blog_urls))
]
