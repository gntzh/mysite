import os
from types import MethodType

from django.core.exceptions import ImproperlyConfigured
from django.template.loader import render_to_string
from django.utils.functional import cached_property
from jieba.analyse import ChineseAnalyzer
from whoosh.filedb.filestore import FileStorage
from whoosh.highlight import Highlighter, HtmlFormatter, ContextFragmenter, WholeFragmenter
from whoosh.index import open_dir, create_in, exists, exists_in


class SearchBackend:
    def __init__(self, model, indexdir, indexname, schema=None):
        self.schema = schema
        self.indexdir = indexdir
        self.indexname = indexname
        self.model = model

        if not os.path.exists(self.indexdir):
            os.mkdir(self.indexdir)
        self.storage = FileStorage(self.indexdir)

        if self.schema is None:
            self.index = self.storage.open_index(indexname=indexname)
            self.schema = self.index.schema
        else:
            self.index = self.storage.create_index(
                schema, indexname=indexname)

    def build_index(self, objects):
        for obj in objects:
            writer = self.index.writer()
            doc = {}
            for field_name, field in self.model._fields.items():
                if field.template_path is not None:
                    doc[field_name] = render_to_string(
                        field.template_path, {'object': obj})
                else:
                    doc[field_name] = str(getattr(obj, field.model_attr, None))
            writer.update_document(**doc)
            writer.commit()


analyzer = ChineseAnalyzer()
fragmenter = ContextFragmenter()
whole_fragmenter = WholeFragmenter()
formatter = HtmlFormatter(
    tagname='span', classname='search-match', termclass='match-term')


def highlight_hit_whole(self, **kwargs):
    self.fragmenter = whole_fragmenter
    try:
        return self.highlight_hit(**kwargs)
    finally:
        self.fragmenter = fragmenter


Highlighter.highlight_hit_whole = highlight_hit_whole

highlighter = Highlighter(fragmenter, formatter=formatter, )
