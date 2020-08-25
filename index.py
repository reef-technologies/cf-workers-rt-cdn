######################################################################
#
# File: index.py
#
# Cloudflare Worker CDN
#
# Copyright (c) 2020, Reef Technologies. All Rights Reserved.
#
######################################################################


async def handleRequest(request):
    url = __new__(URL(request.url))
    new_url = request.url[len(url.origin + PREFIX):]
    if not new_url.startswith('https://') and not new_url.startswith('http://'):
        new_url = url.origin + '/' + new_url
    request = __new__(Request(new_url, request))
    return await fetch(request)


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
