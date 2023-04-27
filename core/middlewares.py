import re


class HTMLOptimize:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if 'text/html' in response.get('Content-Type', ''):
            new_content = re.sub(r'\n\s*?\n', lambda *_: '\n', response.content.decode()) # noqa
            response.content = new_content.encode()
            response["Content-Length"] = len(response.content)
        return response
