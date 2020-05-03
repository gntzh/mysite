from django.template.loader import render_to_string
from jieba.analyse import ChineseAnalyzer
from whoosh.fields import Schema, ID, TEXT


analyzer = ChineseAnalyzer()


class Field(object):
    def __init__(self, model_attr=None, whoosh_field=None, template_path=None, **to_woosh):
        self.model_attr = model_attr
        if whoosh_field in (TEXT, None):
            whoosh_field = TEXT
            to_woosh.setdefault('analyzer', analyzer)
        self.whoosh_field = whoosh_field(**to_woosh)
        self.template_path = template_path


class ModelMetaclass(type):
    def __new__(cls, name, bases, attrs):
        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)

        fields = {}
        schema = Schema()

        attrs['pk'] = Field('pk', ID, unique=True, stored=True)
        for k, v in attrs.items():
            if isinstance(v, Field):
                v.model_attr = v.model_attr or k
                fields[k] = v
                schema.add(k, v.whoosh_field)

        attrs['_fields'] = fields
        attrs['_schema'] = schema
        attrs.setdefault('indexname', attrs['model']._meta.db_table)

        return type.__new__(cls, name, bases, attrs)


class Model(object, metaclass=ModelMetaclass):
    pass
