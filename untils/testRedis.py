import django_redis
from blog import models


# 将某手机号的验证码存入redis
def saveCode(number, code):
    CACHE = django_redis.get_redis_connection()  # 获取redis连接
    codeKey = "phone:" + number  # 生成key值
    CACHE.set(codeKey, code, 60)  # 将验证码保存到redis中
    CACHE.close()  # 关闭连接


# 从redis得到已存的手机号的验证码
def getCode(codeKey):
    CACHE = django_redis.get_redis_connection()
    value = CACHE.get(codeKey).decode()
    CACHE.close()
    return value


# zincrby方法表示:为有序集 Article-clicks 的成员 article_id 的 score 值加上增量 count
# 记录点击的次数的方法
def record_up(article_id, count):
    CACHE = django_redis.get_redis_connection()  # 获取redis连接
    print("---------------")
    print(article_id)
    print(count)
    CACHE.zincrby('Article-Ups', count, article_id)
    print("111111111111111111111111111111")
    CACHE.close()


# 获取排行前num位的数据
def get_top_n_articles(num):
    CACHE = django_redis.get_redis_connection()  # 获取redis连接
    # zrevrange key start stop [WITHSCORES]
    # 返回有序集 key 中，指定区间内的成员
    article_ranking = CACHE.zrange("Article-Ups", 0, -1, desc=True)[:num]   #从sorted_set里面取出排名前num(参数)的num个对象，列表返回，列表的元素是articleid，而不是article本身
    article_ranking_ids = [int(id) for id in article_ranking]   #article_id是str，把str转成int。
    most_viewed = list(models.Article.objects.filter(nid__in=article_ranking_ids)) #拿着10个article_id组成的列表筛选出10个article的列表，filter返回的结果又成乱序
    most_viewed.sort(key=lambda x: article_ranking_ids.index(x.nid))    #对10个article的列表按阅读量重新排序。
    print(most_viewed)
    CACHE.close()
    return most_viewed
