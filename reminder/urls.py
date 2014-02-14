from django.conf.urls import patterns, url
from reminder import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^submit', views.submit, name='submit'),
	url(r'^enterpass', views.enterpass, name='enterpass'),
	url(r'^testpass', views.testpass, name='testpass'),
	url(r'^email_confirmation', views.email_confirmation, name='email_confirmation'),
)