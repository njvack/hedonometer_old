from django.conf.urls.defaults import *
from django.views.generic import TemplateView

from texter import views

urlpatterns = patterns(''
    ,url(r'^incoming$', views.IncomingView.as_view())
)