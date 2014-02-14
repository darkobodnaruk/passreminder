from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'passreminder.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'reminder.views.index', name='home'),
	url(r'^reminder/', include('reminder.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
