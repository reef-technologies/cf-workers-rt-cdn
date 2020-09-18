######################################################################
#
# File: index.py
#
# Cloudflare Worker CDN
#
# Copyright (c) 2020, Reef Technologies. All Rights Reserved.
#
######################################################################


from .settings import config


def log(*args):
    console.log(*args)



class SimpleRequest:
    def __init__(self, request, url):
        self.request = request
        self.url = url

    async def fetch(self, response):
        return await fetch(__new__(Request(self.url, self.request)))


class Cdn:
    def __init__(self, request):
        self.request = request

        self.url = self._parse_url(self.request)
        log(self.request.url, "url:", self.url)

    def requests(self):
        yield SimpleRequest(self.request, self.url)

    @classmethod
    def _parse_url(cls, request):
        url = __new__(URL(request.url))

        if url.host not in config.CDN_ALLOWED_HOSTS:
            raise Exception('host is not allowed')

        new_url = request.url[len(url.origin + config.CDN_PREFIX):]
        if not new_url.startswith('https:') and not new_url.startswith('http:'):
            new_url = url.origin + '/' + new_url

        return __new__(URL(new_url))


async def handleRequest(request):
    cdn = Cdn(request)
    response = None
    for request in cdn.requests():
        response = await request.fetch(response)
    return response


async def handleEvent(event):
    try:
        return await handleRequest(event.request)
    except (object) as exc:
        # TODO: enable Sentry
        console.error(exc)
        if hasattr(exc, 'message'):
            error = exc.message
        else:
            error = str(exc)
        return __new__(Response(JSON.stringify({'error': error}), {
            'status': 500,
            'headers': {'content-type' : 'text/json'},
        }))


addEventListener('fetch', lambda event: event.respondWith(handleEvent(event)))
