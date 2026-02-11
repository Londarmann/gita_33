import time
from django.conf import settings
from django.http import HttpResponse


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        duration = time.time() - start_time

        user = request.user.username if request.user.is_authenticated else "Anonymous"

        print(
            f"{request.method} {request.path} --  User: {user} --  Duration: {duration} seconds")
        return response


# MAINTENANCE_MODE
class MaintenanceModeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        maintanance = getattr(settings, "MAINTENANCE_MODE", False)

        if maintanance:
            if request.path.startswith("/admin/"):
                return self.get_response(request)
            if request.user.is_authenticated and request.user.is_superuser:
                return self.get_response(request)

            return HttpResponse("""
            <html>
            <body style="text-align: center; padding: 50px">
            <h1>საიტი მიუწვდომელია</h1>
            <p>მიმდინარეობს ტექნიკური სამუშაოები</p>
            </body>
            </html>

            """, status=503)
        return self.get_response(request)