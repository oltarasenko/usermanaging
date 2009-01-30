from django.conf.urls.defaults import *
import django.contrib.auth.views
from views import start_page, logout_page, register_page


from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       (r'^$', start_page),
                       (r'logout/$', logout_page),
                       (r'^login/$', 'django.contrib.auth.views.login'),
                       (r'register/$', register_page),
                       (r'^admin/(.*)', admin.site.root),
                       (r'^password_reset/done/$',
                        'django.contrib.auth.views.password_reset_complete',
                        {'template_name':
                         'registration/password_reset_complete.html'}),
                       (r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
                        'django.contrib.auth.views.password_reset_confirm'),
                       (r'^resend/$',
                        'django.contrib.auth.views.password_reset',
                        {'template_name':
                             'registration/password_reset_form.html',
                         'email_template_name':
                             'registration/password_reset_email.html',
                         'post_reset_redirect':
                             '/message-sent'}),
                       )
