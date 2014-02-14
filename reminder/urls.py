from django.conf.urls import patterns, url
from reminder import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index')
)