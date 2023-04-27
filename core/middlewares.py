import re


class HTMLOptimize:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        new_content = re.sub(r'(?m)^\s*$\n?', '', response.content.decode())
        response.content = new_content.encode()
        response["Content-Length"] = len(response.content)
        return response
