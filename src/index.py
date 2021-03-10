######################################################################
#
# File: src/index.py
#
# Cloudflare Worker CDN
#
# Copyright (c) 2020, Reef Technologies. All Rights Reserved.
#
######################################################################

import re

from src import config
from src import logger
from src import mimetypes


class CdnError(Exception):
    def __init__(self, message, status_code=500):
        self.message = message
        self.status_code = status_code


class CdnRouter:
    routes = []

    def __init__(self, request):
        self.request = request
        self.resource = self._get_resource(self.request.url)

        logger.debug('Router:', self)

    def __repr__(self):
        return '{}(request={})'.format(self.__class__.__name__, self.request)

    async def fetch(self):
        return await self.resource.fetch(self.request)

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
                return klass(raw_url, **m.groupdict())

        raise CdnError('wrong URL: ' + raw_url, 400)


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
    __pragma__('kwargs')
    def __init__(self, url, origin_url):
        self.url = url
        self.origin_url = self._get_origin_url(origin_url, self.url)

        logger.debug('Resource:', self)
    __pragma__('nokwargs')

    def __repr__(self):
        return '{}(url={}, origin_url={})'.format(self.__class__.__name__,
            self.url, self.origin_url)

    async def fetch(self, request, url=None):
        if url is None:
            url = self.origin_url

        logger.debug('{}.fetch request:'.format(self.__class__.__name__), request)
        logger.debug('{}.fetch url:'.format(self.__class__.__name__), url)

        response = await fetch(url, request)

        logger.debug('{}.fetch response:'.format(self.__class__.__name__), response)

        return response

    @classmethod
    def _get_origin_url(cls, origin_raw_url, raw_url):
        url = __new__(URL(raw_url))

        if not origin_raw_url.startswith('https:') and not origin_raw_url.startswith('http:'):
            origin_raw_url = url.origin + '/' + origin_raw_url

        origin_url = __new__(URL(origin_raw_url))

        if config.ALLOWED_HOSTS:
            if origin_url.host not in config.ALLOWED_HOSTS:
                raise CdnError('host is not allowed: ' + origin_url.host, 403)

        return origin_url


@route(CdnRouter, r'{}/cache/(?P<origin_url>.*)'.format(config.PREFIX))
class CacheResource(Resource):
    pass


@route(CdnRouter, '{}/image/width=(?P<width>\d+|auto|orig)/(?P<origin_url>.*)'.format(config.PREFIX))
class ImageResource(Resource):
    __pragma__('kwargs')
    def __init__(self, url, origin_url, width):
        self.width = width
        self.format = None  # TODO: add a possibility to set from URL, not only from HTTP Accept
        Resource.__init__(self, url, origin_url)
    __pragma__('nokwargs')

    async def fetch(self, request, url=None, init=None):
        self.width = self._get_width(request)
        self.format = self._get_format(request)
        url = self._transform_url()

        if config.SERVER_PREFIX:
            request_head = __new__(Request(request, {'method': 'HEAD', 'cf': {'cacheTtl': 0}}))
            response = await Resource.fetch(self, request_head, url)
            if response.status == 404:
                response = await self.fetch_via_server(request)
            else:
                response = await Resource.fetch(self, request, url)
        else:
            response = await Resource.fetch(self, request, url)

        return response

    async def fetch_via_server(self, request):
        url = '{}/images'.format(config.SERVER_PREFIX)

        request_server = __new__(Request(url, {
            'method': 'POST',
            'headers': {
                'content-type': 'application/json',
                config.SERVER_API_TOKEN_HEADER: 'ApiKey ' + config.SERVER_API_TOKEN,
            },
            'body': JSON.stringify({
                'origin': self.origin_url,
                'width': self.width,
                'format': self.format,
                'force': True,
            })
        }))
        response = await Resource.fetch(self, request_server, url)

        if response.status == 200:
            body = await response.json()
            url = body['url']
            return await Resource.fetch(self, request, url)

        return response

    def _transform_url(self):
        # If width can not be fetched, fallback to origin
        if self.width is None:
            return self.origin_url

        # Change the URL to include width
        origin_url = __new__(URL(self.origin_url))
        pathname_split = origin_url.pathname.split('/')
        orig_filename = pathname_split[len(pathname_split)-1]
        dirname = '{}-cdn'.format(orig_filename)
        filename = self._get_filename(orig_filename)
        pathname_split.pop()
        pathname_split.append(dirname)
        pathname_split.append(filename)
        origin_url.pathname = '/'.join(pathname_split)

        return origin_url.toString()

    def _get_width(self, request):
        if self.width == 'auto':  # If auto, use Client Hints
            width = request.headers.js_get('Width') or None
        elif self.width == 'orig':
            width = None
        else:
            width = self.width

        # For allowed widths, return the value from the list
        if config.ALLOWED_WIDTHS and width is not None:
            width = int(width)
            for allowed_width in config.ALLOWED_WIDTHS:
                allowed_width = int(allowed_width)
                if allowed_width >= width:
                    return str(allowed_width)

            # No proper width found on the list
            return None

        # All widths are allowed, so return exact value or None to fallback to the origin
        return width

    def _get_format(self, request):
        accept = request.headers.js_get('Accept') or None
        # For allowed formats, pick the first one that exist in Accept HTTP header
        if config.ALLOWED_FORMATS and accept is not None:
            for allowed_format in config.ALLOWED_FORMATS:
                mimetype = mimetypes.guess_type(allowed_format)
                if mimetype is not None and mimetype in accept:
                    return allowed_format

        # Format can't be calculated from HTTP Accept header, use the file extension
        return None

    def _get_filename(self, filename):
        # Set marker
        if self.width is not None:
            marker = '-{}w'.format(self.width)
        else:
            marker = ''

        # Set extension
        if '.' in filename:
            basename, ext = filename.rsplit('.', maxsplit=1)
            if not basename:
                basename = filename
                ext = self.format or ''
            else:
                ext = self.format or ext.lower()
        else:
            basename = filename
            ext = self.format or ''

        if ext:
            ext = '.' + ext

        return ''.join([basename, marker, ext])


async def handleRequest(request):
    cdn = CdnRouter(request)
    return await cdn.fetch()


async def handleEvent(event):
    logger.debug('Config:', config)

    try:
        return await handleRequest(event.request)
    except (object) as exc:
        # TODO: enable Sentry
        if hasattr(exc, 'message'):
            error = exc.message
        else:
            error = str(exc)
        body = JSON.stringify({'error': error})
        logger.error('Error:', exc, body)
        return __new__(Response(body, {
            'status': exc.status_code or 500,
            'headers': {'content-type': 'application/json'},
        }))


addEventListener('fetch', lambda event: event.respondWith(handleEvent(event)))
