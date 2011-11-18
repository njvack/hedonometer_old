from django.conf.urls.defaults import patterns, include, url

import texter.urls

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url('', include(texter.urls.urlpatterns)),
)
