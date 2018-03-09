from django.conf.urls import url, include
from . import views
from django_filters.views import FilterView
from django.views.generic import TemplateView
from .filters import SearchFilter

urlpatterns = [
    url(r'^(?P<page>[0-9]+)/$', views.index, name="index"),
    url(r'^$', views.index_dim, name="sosatt"),
    url(r'^ask/$', views.AskView.as_view(), name="ask"),
    url(r'^topics/(?P<page>[0-9]+)/$', views.topics_view, name="topics"),

    url(r'^question/(?P<id>[0-9]+)/$', views.question_view, name="question"),

    url(r'^answer1/(?P<id>[0-9]+)/$', views.answer_view, name="answer1"),
    url(r'^answer2/(?P<id>[0-9]+)/$', views.answer2_view, name="answer2"),

    url(r'^answer/(?P<id>[0-9]+)/$', views.AnswerView.as_view(), name="answer"),

    url(r'^topic/(?P<id>[0-9]+)/$', views.topic_no_page, name="topic"),
    url(r'^topic/(?P<id>[0-9]+)/(?P<page>[0-9]+)/$', views.topic_view, name="topic"),

    url(r'^follow/$', views.follow_view, name="follow"),
    url(r'^search/$', FilterView.as_view(filterset_class=SearchFilter, template_name='question/arama_list.html'), name='search'),

    url(r'^comment/(?P<id>[0-9]+)/$', views.CommentView.as_view(), name="comment"),
    url(r'^comment2/(?P<id>[0-9]+)/$', views.Comment2View.as_view(), name="comment2"),
    url(r'^qlike/(?P<id>[0-9]+)/$', views.q_like_view, name="qlike"),
    url(r'^qdislike/(?P<id>[0-9]+)/$', views.q_dislike_view, name="qdislike"),

    url(r'^alike/(?P<id>[0-9]+)/$', views.a_like_view, name="alike"),
    url(r'^adislike/(?P<id>[0-9]+)/$', views.a_dislike_view, name="adislike"),

    url(r'^delete/(?P<id>[0-9]+)/(?P<page>[0-9]+)/$', views.question_delete_view,name="delete"),

    url(r'^adelete/(?P<id>[0-9]+)/(?P<page>[0-9]+)/$', views.answer_delete_view,name="adelete"),
    url(r'^cdelete/(?P<id>[0-9]+)/(?P<page>[0-9]+)/$', views.comment_delete_view,name="cdelete"),

    url(r'^questionEdit/(?P<id>[0-9]+)/$', views.QuestionEditView.as_view(), name="qedit"),
    url(r'^answerEdit/(?P<id>[0-9]+)/$', views.AnswerEditView.as_view(), name="aedit"),
    url(r'^commentEdit/(?P<id>[0-9]+)/$', views.CommentEditView.as_view(), name="cedit"),


]
