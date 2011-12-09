
from django.http import HttpResponse
from django.views.generic import TemplateView

import logging
logger = logging.getLogger('texter')

import tropo # Temporary! Abstract this.

class IncomingView(TemplateView):
    
    def dispatch(self, *args, **kwargs):
        logger.debug('This is IncomingView#dispatch()')
        resp = HttpResponse(content_type='application/json')
        t = tropo.Tropo()
        t.say('This is a response')
        resp.write(t.RenderJson())
        return resp

