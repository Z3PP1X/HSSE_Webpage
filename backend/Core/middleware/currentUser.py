import threading
from django.utils.deprecation import MiddlewareMixin

_user = threading.local()


def get_current_user():

    return getattr(_user, 'user', None)


class CurrentUserMiddleware(MiddlewareMixin):

    def process_request(self, request):
        _user.user = request.user

    def process_response(self, request, response):

        _user.user = None
        return response

    