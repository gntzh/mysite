from haystack import indexes
from blog.models import Post


class PostIndex(indexes.SearchIndex, indexes.Indexable):
    # indexed=True, stored=True, 默认所有字段都存储并索引, 可以将index=True用来展示以避免访问数据库(load_all), 但是会占用更多得空间
    # document=False, 改为True(有且只能有一个)用于形成语料库, 进行搜索
    # use_template=False, 改为True, 则字段内容由模板决定
    # 良好的document应不包含HTML代码,日期类型,数字类型, 包含title,author,content,tags,category
    text = indexes.CharField(document=True, use_template=True)
    # 其他document=False的字段, 用于过滤,排序, 缩小搜索范围, 一般添加作者,分类,日期类型,数字类型
    # model_attr用于确定对应的字段, 可以使用关系字段'author__first_name'
    # id, django_ct, django_id & content是haystack的保留字段
    author = indexes.CharField(model_attr='author')
    created = indexes.DateTimeField(model_attr='created')

    def get_model(self):
        return Post

    def index_queryset(self, using=None):
        # 更新整个模型的索引时使用
        return self.get_model().public.all()

    # 定义prepare_FOO(self, object), 可以由方法返回值确定字段值, 返回一个字符串,元组,列表,字典
    # 在SearchField的prepare方法调用后被调用, 可以访问self.prepare_data
    # prepare(self, object)方法用于返回最后的数据, 应返回一个字典
    def prepare_author(self, obj):
        return obj.author.nickname or obj.author.username
