######################################################################
#
# File: src/mimetypes.py
#
# Cloudflare Worker CDN
#
# Copyright (c) 2020, Reef Technologies. All Rights Reserved.
#
######################################################################

_MIMETYPES = {
    'jpeg': 'image/jpeg',
    'jpg': 'image/jpeg',
    'png': 'image/png',
    'tif': 'image/tiff',
    'tiff': 'image/tiff',
    'wbmp': 'image/vnd.wap.wbmp',
    'ico': 'image/x-icon',
    'jng': 'image/x-jng',
    'bmp': 'image/x-ms-bmp',
    'svg': 'image/svg+xml',
    'webp': 'image/webp',
}


def guess_type(ext):
    if ext not in _MIMETYPES:
        return None
    return _MIMETYPES[ext]
