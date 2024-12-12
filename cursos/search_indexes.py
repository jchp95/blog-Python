from haystack import indexes
from .models import Curso



class CursosIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Curso

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
