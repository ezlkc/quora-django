from django import forms
from .models import Question
import django_filters


class SearchFilter(django_filters.FilterSet):

    content = django_filters.CharFilter(lookup_expr='icontains')
    #groups = django_filters.ModelMultipleChoiceFilter(queryset=Group.objects.all(), widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Question
        fields = ['content']
