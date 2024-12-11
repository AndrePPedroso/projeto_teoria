class LanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if "language" not in request.session:
            request.session["language"] = "pt" 

        response = self.get_response(request)
        return response
