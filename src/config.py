######################################################################
#
# File: src/config.py
#
# Cloudflare Worker CDN
#
# Copyright (c) 2020, Reef Technologies. All Rights Reserved.
#
######################################################################

# Below variables are fetched from the Wrangler variables
# You can change it in .env or directly in wrangler.toml

ENV = CDN_ENV
DEBUG = CDN_DEBUG != '0'  
PREFIX = CDN_PREFIX
SERVER_PREFIX = CDN_SERVER_PREFIX
SERVER_API_TOKEN_HEADER = CDN_SERVER_API_TOKEN_HEADER
SERVER_API_TOKEN = CDN_SERVER_API_TOKEN

ALLOWED_HOSTS = CDN_ALLOWED_HOSTS.split(',')
if ALLOWED_HOSTS[0] == '':
    ALLOWED_HOSTS = None

ALLOWED_WIDTHS = CDN_ALLOWED_WIDTHS.split(',')
if ALLOWED_WIDTHS[0] == '':
    ALLOWED_WIDTHS = None

ALLOWED_FORMATS = CDN_ALLOWED_FORMATS.split(',')
if ALLOWED_FORMATS[0] == '':
    ALLOWED_FORMATS = None
