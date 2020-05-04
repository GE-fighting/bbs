from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


# 用户信息表
class UserInfo(AbstractUser):
    nid = models.AutoField(primary_key=True)
    phone = models.CharField(max_length=11, null=True, unique=True)
    profile = models.CharField(max_length=128,null=True)
    avatar = models.FileField(upload_to="avatars/", default="avatars/default.jpg", verbose_name="头像")
    create_time = models.DateTimeField(auto_now_add=True)
    blog = models.OneToOneField(to="Blog", to_field="nid", null=True)

    def __str__(self):  # 在显示对该类对象的描述，可用在admin站点中
        return self.username

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name


# 用户关注表
class UserConcern(models.Model):
    nid = models.AutoField(primary_key=True)  # 主键字段
    concerned = models.ForeignKey(to="UserInfo", to_field="nid", related_name="concerned_user")  # 被关注者
    concern = models.ForeignKey(to="UserInfo", to_field="nid", related_name="concern_user")  # 关注者

    def __str__(self):
        return self.concerned.username + "<---" + self.concern.username

    class Meta:
        unique_together = (("concerned", "concern"),)  # 联合主键
        verbose_name = "用户关注"
        verbose_name_plural = verbose_name


# 博客信息表
class Blog(models.Model):
    '''
    博客信息
    '''
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)  # 个人博客标题
    site = models.CharField(max_length=32, unique=True)  # 个人博客后缀
    theme = models.CharField(max_length=32)  # 博客主题
    profile = models.CharField(max_length=128,null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "blog 站点"
        verbose_name_plural = verbose_name

#文章分类表
class Category(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32)  # 分类标题
    blog = models.ForeignKey(to="Blog", to_field="nid")  # 外键关联博客，一个博客站点可以有很多分类

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "文章分类"
        verbose_name_plural = verbose_name

#文章标签表
class Tag(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32)  # 标签名
    blog = models.ForeignKey(to="Blog", to_field="nid")  # 所属博客

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "文章标签"
        verbose_name_plural = verbose_name

#文章表
class Article(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)  # 文章标题
    desc = models.CharField(max_length=255)  # 文章描述
    create_time = models.DateTimeField(auto_now_add=True)  # 创建时间
    comment_count = models.IntegerField(verbose_name="评论数", default=0)  # 评论数
    up_count = models.IntegerField(verbose_name="点赞数", default=0)  # 点赞数
    down_count = models.IntegerField(verbose_name="踩数", default=0)  # 踩数
    category = models.ForeignKey(to="Category", to_field="nid", null=True)
    user = models.ForeignKey(to="UserInfo", to_field="nid")
    tags = models.ManyToManyField(  # 中介模型
        to="Tag",
        through="ArticleToTag",
        through_fields=("article", "tag"),  # 注意顺序
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "文章"
        verbose_name_plural = verbose_name


class ArticleDetail(models.Model):
    nid = models.AutoField(primary_key=True)
    content = models.TextField()
    article = models.OneToOneField(to="Article", to_field="nid")

    class Meta:
        verbose_name = "文章详情"
        verbose_name_plural = verbose_name


class ArticleToTag(models.Model):
    nid = models.AutoField(primary_key=True)
    article = models.ForeignKey(to="Article", to_field="nid")
    tag = models.ForeignKey(to="Tag", to_field="nid")

    def __str__(self):
        return "{}-{}".format(self.article.title, self.tag.title)

    class Meta:
        unique_together = (("article", "tag"),)
        verbose_name = "文章-标签"
        verbose_name_plural = verbose_name


class ArticleUpDown(models.Model):
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey(to="UserInfo", to_field="nid")
    article = models.ForeignKey(to="Article", to_field="nid")
    is_up = models.BooleanField(default=True)

    class Meta:
        unique_together = (("article", "user"),)  # 联合主键
        verbose_name = "文章点赞"
        verbose_name_plural = verbose_name


class Comments(models.Model):
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey(to="UserInfo", to_field="nid")
    article = models.ForeignKey(to="Article", to_field="nid")
    content = models.CharField(max_length=225)  # 评论内容
    create_time = models.DateTimeField(auto_now_add=True)
    parent_comment = models.ForeignKey("self", null=True, blank=True)  # blank属性设置 表明在admin里面是否可以不填

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = "文章评论"
        verbose_name_plural = verbose_name
