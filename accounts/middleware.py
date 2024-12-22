from django.shortcuts import redirect
from django.conf import settings
from django.urls import resolve

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            current_path = resolve(request.path_info).url_name
            if current_path not in ['login'] and not request.path.startswith(settings.STATIC_URL):
                return redirect(settings.LOGIN_URL)
        return self.get_response(request)
