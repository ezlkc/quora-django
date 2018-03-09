from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^signup/$', views.SignUpView.as_view(), name="signup"),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name="activate"),
    url(r'^login/$', views.LoginView.as_view(), name="login"),
    url(r'^logout/$', views.logout_view, name="logout"),

    url(r'^u/(?P<username>[\w]+)/(?P<page>[0-9]+)/$', views.profile_view, name="profile"),
    url(r'^u/(?P<username>[\w]+)/$', views.profile_view_2, name="profile"),

    url(r'^answers/(?P<username>[\w]+)/(?P<page>[0-9]+)/$', views.answers_view, name="answers"),
    url(r'^answers/(?P<username>[\w]+)/$', views.answers_view_2, name="answers"),

    url(r'^commnets/(?P<username>[\w]+)/(?P<page>[0-9]+)/$', views.comments_view, name="commnets"),
    url(r'^commnets/(?P<username>[\w]+)/$', views.comments_view_2, name="commnets"),


    url(r'^edit/$', views.EditView.as_view(), name="edit"),



]
