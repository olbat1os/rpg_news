from django_filters import FilterSet, DateTimeFilter
from .models import *
from django.forms import DateTimeInput

class PostFilter(FilterSet):
    added_after = DateTimeFilter(
        field_name='dateCreation',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},

        ),
    )

    class Meta:
        model = Post
        fields = {
            'categoryType': ['exact'],
            'title': ['icontains'],
        }

class CommFilter(FilterSet):
    class Meta:

        model = Comment
        fields = {
            'message'
        }

    def __init__(self, *args, **kwargs):
        super(CommFilter, self).__init__(*args, **kwargs)
        self.filters['message'].queryset = Post.objects.filter(author__id=kwargs['request'])


#class MsgFilter(FilterSet):
  # class Meta:
       # В Meta классе мы должны указать Django модель,
       # в которой будем фильтровать записи.
       #model = Post
       # В fields мы описываем по каким полям модели
       # будет производиться фильтрация.
       #fields = {
           # поиск по названию
           #'title': ['icontains'],
       #}
