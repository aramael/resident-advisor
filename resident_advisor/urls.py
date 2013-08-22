from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'resident_advisor.views.home', name='home'),

    # Call Tree Pages
    url(r'^calltree/$', 'resident_advisor.views.call_tree_home', name='call_tree_home'),
    url(r'^calltree/profile/me$', 'resident_advisor.views.call_tree_proflie', name='call_tree_proflie'),

    url(r'^admin/', include(admin.site.urls)),
)