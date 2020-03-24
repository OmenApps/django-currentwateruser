from django.conf import settings
from threading import local

WATERUSER_ATTR_NAME = getattr(settings, 'LOCAL_WATERUSER_ATTR_NAME', '_current_wateruser')

_thread_locals = local()


def _do_set_current_wateruser(wateruser_fun):
    setattr(_thread_locals, WATERUSER_ATTR_NAME, wateruser_fun.__get__(wateruser_fun, local))


def _set_current_wateruser(wateruser=None):
    '''
    Sets current wateruser in local thread.

    Can be used as a hook e.g. for shell jobs (when request object is not
    available).
    '''
    _do_set_current_wateruser(lambda self: wateruser)


class ThreadLocalWaterUserMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # request.organization_context closure; asserts laziness;
        # memorization is implemented in
        # request.organization_context (non-data descriptor)
        _do_set_current_wateruser(lambda self: getattr(request, 'organization_context', None))
        response = self.get_response(request)
        return response


def get_current_wateruser():
    current_wateruser = getattr(_thread_locals, WATERUSER_ATTR_NAME, None)
    if callable(current_wateruser):
        return current_wateruser()
    return current_wateruser


def get_current_verified_wateruser():
    current_wateruser = get_current_wateruser()
    if current_wateruser is None:
        return None
    if isinstance(current_wateruser, WaterUser):
        return current_wateruser
    return None
