from django.conf.urls import patterns, url
from reminder import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^submit', views.submit, name='submit'),
	url(r'^enterpass', views.enterpass, name='enterpass'),
)