from django.conf.urls.defaults import *
import django.contrib.auth.views


from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
                       url(r'^', include('loginreg.urls')),
                       
                       )
