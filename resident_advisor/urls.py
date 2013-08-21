from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'resident_advisor.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
)