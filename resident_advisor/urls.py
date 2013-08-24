from django.conf.urls import patterns, include, url
from django.contrib.auth import views as auth_views
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'resident_advisor.views.home', name='home'),

    # User Pages
    url(r'^users/$', 'resident_advisor.views.users_home', name='users_home'),

    # Call Tree Pages
    url(r'^calltree/$', 'resident_advisor.views.call_tree_home', name='call_tree_home'),
    url(r'^calltree/profile/me/$', 'resident_advisor.views.call_tree_proflie', name='call_tree_proflie'),

    # Call Tree Twilio Pages
    url(r'^twilio/calltree/recieve/$', 'resident_advisor.apps.call_tree.views.call_recieve', name='call_tree_recieve_call'),
    url(r'^twilio/calltree/send/$', 'resident_advisor.apps.call_tree.views.outgoing_call', name='call_tree_outgoing_call'),
    url(r'^twilio/calltree/connect/$', 'resident_advisor.apps.call_tree.views.conference_connect', name='call_tree_conference_connect'),

    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    # Account Pages
    url(r'^login/$',
       auth_views.login,
       {'template_name': 'users/login.html'},
       name='auth_login'),
    url(r'^logout/$',
       auth_views.logout,
       {'template_name': 'users/logout.html'},
       name='auth_logout'),
    url(r'^password/change/$',
       auth_views.password_change,
        {'template_name': 'users/password_change_form.html'},
       name='auth_password_change'),
    url(r'^password/change/done/$',
       auth_views.password_change_done,
       {'template_name': 'users/password_change_done.html'},
       name='auth_password_change_done'),
    url(r'^password/reset/$',
       auth_views.password_reset,
       {'template_name': 'users/password_reset_form.html',
        'email_template_name': 'users/password_reset_email.html'},
       name='auth_password_reset'),
    url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
       auth_views.password_reset_confirm,
       {'template_name': 'users/password_reset_confirm.html'},
       name='auth_password_reset_confirm'),
    url(r'^password/reset/complete/$',
       auth_views.password_reset_complete,
       {'template_name': 'users/password_reset_complete.html'},
       name='auth_password_reset_complete'),
    url(r'^password/reset/done/$',
       auth_views.password_reset_done,
       {'template_name': 'users/password_reset_done.html'},
       name='auth_password_reset_done'),
)