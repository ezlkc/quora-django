from django import forms
from .models import Question, Answer, Comment

class AskForm(forms.ModelForm):
    content = forms.CharField(min_length=40, max_length=200, widget=forms.Textarea(attrs={'class': 'textarea', 'style': 'resize:none', 'rows': '2'}))

    class Meta:
        model = Question
        fields = ['content','picture']

    def __init__(self, *args, **kwargs):
        if kwargs:
            content = kwargs.pop("content")  # kullanıcıdan, views.py'den aktarılan parametredir

            super(AskForm, self).__init__(*args, **kwargs)
            self.fields['content'] = forms.CharField(min_length=40, max_length=200, widget=forms.Textarea(attrs={'class': 'textarea', 'style': 'resize:none', 'rows': '2','value': content}))

        else:
            super(AskForm, self).__init__(*args, **kwargs)

class AnswerForm(forms.ModelForm):
    content = forms.CharField(min_length=40, max_length=3000, widget=forms.Textarea(attrs={'class': 'textarea', 'style': 'resize:none', 'rows': '12'}))

    class Meta:
        model = Answer
        fields = ['content', 'picture']
    def __init__(self, *args, **kwargs):
        if kwargs:
            content = kwargs.pop("content")  # kullanıcıdan, views.py'den aktarılan parametredir

            super(AnswerForm, self).__init__(*args, **kwargs)
            self.fields['content'] = forms.CharField(min_length=40, max_length=3000, widget=forms.Textarea(attrs={'class': 'textarea', 'style': 'resize:none', 'rows': '12','value': content}))

        else:
            super(AnswerForm, self).__init__(*args, **kwargs)

class CommentForm(forms.ModelForm):
    content = forms.CharField(min_length=40, max_length=3000, widget=forms.Textarea(attrs={'class': 'textarea', 'style': 'resize:none', 'rows': '12'}))

    class Meta:
        model = Comment
        fields = ['content', 'picture']

    def __init__(self, *args, **kwargs):
        if kwargs:
            content = kwargs.pop("content")  # kullanıcıdan, views.py'den aktarılan parametredir

            super(CommentForm, self).__init__(*args, **kwargs)
            self.fields['content'] = forms.CharField(min_length=40, max_length=3000, widget=forms.Textarea(attrs={'class': 'textarea', 'style': 'resize:none', 'rows': '12','value': content}))

        else:
            super(CommentForm, self).__init__(*args, **kwargs)


