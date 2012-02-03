"""
Simply copies the X_FORWARDED crap into HTTP_HOST and SERVER_NAME.
"""

class SetHostname(object):
    
    def process_request(self, request):
        request.META['HTTP_HOST'] = request.META['HTTP_X_FORWARDED_HOST']
        request.META['SERVER_NAME'] = request.META['HTTP_X_FORWARDED_SERVER']
        