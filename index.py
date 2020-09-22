######################################################################
#
# File: index.py
#
# Cloudflare Worker CDN
#
# Copyright (c) 2020, Reef Technologies. All Rights Reserved.
#
######################################################################


from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    CDN_ALLOWED_HOSTS = JSON.parse(CDN_ALLOWED_HOSTS)
    CDN_PREFIX = CDN_PREFIX


config = Config()


def log(*args):
    console.log(*args)


class CacheEndpoint:
    def __init__(self, request, url):
        self.request = request
        self.url = url
        log('CacheEndpoint url:', self.url)

    async def fetch(self, response):
        return await fetch(__new__(Request(self.url, self.request)))


class CdnError(Exception):
    def __init__(self, message, status_code=500):
        self.message = message
        self.status_code = status_code


class Cdn:
    def __init__(self, request):
        self.request = request
        log('Cdn request:', self.request)
        self.endpoint = self._parse_endpoint(self.request)
        log('Cdn endpoint:', self.endpoint)

    def fetch(self):
        return self.endpoint.fetch()

    @classmethod
    def _parse_endpoint(cls, request):
        url = __new__(URL(request.url))

        new_url = request.url[len(url.origin + config.CDN_PREFIX):]
        if not new_url.startswith('https:') and not new_url.startswith('http:'):
            new_url = url.origin + '/' + new_url

        new_url = __new__(URL(new_url))

        if new_url.host not in config.CDN_ALLOWED_HOSTS:
            raise CdnError('host is not allowed: ' + new_url.host, 403)

        return CacheEndpoint(request, new_url)


async def handleRequest(request):
    cdn = Cdn(request)
    return cdn.fetch()


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
            'status': exc.status_code or 500,
            'headers': {'content-type' : 'text/json'},
        }))


addEventListener('fetch', lambda event: event.respondWith(handleEvent(event)))
