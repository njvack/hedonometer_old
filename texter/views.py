from django.views.generic import TemplateView

import logging
logger = logging.getLogger('texter')

class IncomingView(TemplateView):
    template_name = 'incoming.html'
    
    def dispatch(self, *args, **kwargs):
        logger.debug('This is IncomingView#dispatch()')
        return super(IncomingView, self).dispatch(*args, **kwargs)
        