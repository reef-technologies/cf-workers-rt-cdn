######################################################################
#
# File: index.py
#
# Cloudflare Worker CDN
#
# Copyright (c) 2020, Reef Technologies. All Rights Reserved.
#
######################################################################

import re

import config



def log(*args):
    if config.DEBUG:
        console.log(*args)



class CdnError(Exception):
    def __init__(self, message, status_code=500):
        self.message = message
        self.status_code = status_code


class CdnRouter:
    routes = []

    def __init__(self, request):
        self.request = request
        log('Request:', self.request)
        self.resource = self._get_resource(self.request.url)
        log('Resource:', self.resource)

    def fetch(self):
        return self.resource.fetch(self.request)

    @classmethod
    def _get_pathname(cls, raw_url):
        url = __new__(URL(raw_url))

        return raw_url[len(url.origin):]

    @classmethod
    def _get_resource(cls, raw_url):
        pathname = cls._get_pathname(raw_url)

        for route, klass in cls.routes:
            m = re.fullmatch(route, pathname)
            if m:
                return klass(raw_url, *m.groups())

        raise CdnError('wrong CDN endpoint in URL: ' + raw_url, 400)


def route(router, path):
    def decorator(klass):
        router.routes.append((path, klass))
        __pragma__('kwargs')
        def wrapper(*args, **kwargs):
            return klass(*args, **kwargs)
        __pragma__('nokwargs')
        return wrapper
    return decorator


class Resource:
    def __init__(self, url, origin_url):
        self.url = url
        log('URL:', self.url)
        self.origin_url = self._get_origin_url(origin_url, self.url)
        log('Origin URL:', self.origin_url)

    async def fetch(self, request):
        return await fetch(__new__(Request(self.origin_url, request)))

    @classmethod
    def _get_origin_url(cls, origin_raw_url, raw_url):
        url = __new__(URL(raw_url))

        if not origin_raw_url.startswith('https:') and not origin_raw_url.startswith('http:'):
            origin_raw_url = url.origin + '/' + origin_raw_url

        origin_url = __new__(URL(origin_raw_url))

        if origin_url.host not in config.ALLOWED_HOSTS + [url.origin]:
            raise CdnError('host is not allowed: ' + origin_url.host, 403)

        return origin_url


@route(CdnRouter, r'{}/cache/(.*)'.format(config.PREFIX))
class CacheResource(Resource):
    pass


# @route(CdnRouter, '{}/image/width=(\d+|auto)/(.*)'.format(config.PREFIX))
# class ImageResource(Resource):
#     def __init__(self, url, width, origin_url):
#         Resource.__init__(self, url, origin_url)
#         self._transform_origin_url(width)
#         log('Transformed Origin URL:', self.origin_url)

#     def _transform_origin_url(self, width):
#         origin_url = __new__(URL(self.origin_url))
#         origin_url.pathname += '-w{}'.format(width)
#         self.origin_url = origin_url.toString()


async def handleRequest(request):
    cdn = CdnRouter(request)
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
