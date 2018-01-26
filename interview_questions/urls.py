from django.conf.urls import url

from . import views

app_name = 'interview_questions'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^p/(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^c/add/$', views.AddCommentView.as_view(), name='add_c'),
    url(r'^r/add/$', views.ReplyView.as_view(), name="add_r"),
    url(r'^c/edit/$', views.EditCommentView.as_view(), name='edit_c'),
    url(r'^r/edit/$', views.EditReplyView.as_view(), name='edit_r'),
    url(r'^c/delete/$', views.DeleteCommentView.as_view(), name='delete_c'),
    url(r'^r/delete/$', views.DeleteReplyView.as_view(), name='delete_r'),
    # url(r'^p/vote/$', views.VoteView.as_view(), name='vote_p'),
    url(r'^vote/$', views.VoteView.as_view(), name='vote'),
    url(r'^p/(?P<pk>[0-9]+)/edit/$', views.EditView.as_view(), name='edit'),
    url(r'^p/(?P<pk>[0-9]+)/delete/$', views.DeleteView.as_view(), name='delete'),
    url(r'^p/(?P<pk>[0-9]+)/reply/(?P<comment_id>[0-9]+)/$', views.ReplyView.as_view(), name='reply'),
    url(r'^p/add/$', views.AddView.as_view(), name='add'),
    url(r'^topic/(?P<tp>[\w]+)/$', views.TopicView.as_view(), name='topic')
]
