from django.http import JsonResponse


class AiSiteAuthenticateMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/api/'):
            session = request.session
            if not session.get('logged', False):
                return JsonResponse({'error': 'Session has expired, please login'}, status=401)
        return self.get_response(request)
