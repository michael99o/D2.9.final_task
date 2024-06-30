from django_filters import FilterSet, ChoiceFilter, ModelChoiceFilter, DateTimeFilter
from django.forms import DateTimeInput
from .models import Post, Category
from .resources import CONTENT

class NewsFilter(FilterSet):
    category = ModelChoiceFilter(
        field_name='postcategory__category',
        queryset=Category.objects.all(),
        label='Category',
        empty_label='Any category',

    )
    added_after = DateTimeFilter(
        field_name='date',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        ),
    )

    content = ChoiceFilter(
        field_name = 'content',
        label = 'Тип публикации',
        empty_label = 'Все типы',
        choices = CONTENT
    )

    class Meta:
        model = Post
        fields = {
            'title':['iregex'],
            }

