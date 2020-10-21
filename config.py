######################################################################
#
# File: config.py
#
# Cloudflare Worker CDN
#
# Copyright (c) 2020, Reef Technologies. All Rights Reserved.
#
######################################################################

# Below variables are fetched from the Wrangler variables
# You can change it in .env

ENV = CDN_ENV
DEBUG = CDN_DEBUG != '0'  
PREFIX = CDN_PREFIX

ALLOWED_HOSTS = CDN_ALLOWED_HOSTS.split(',')
if ALLOWED_HOSTS[0] == '':
    ALLOWED_HOSTS = None

ALLOWED_WIDTHS = CDN_ALLOWED_WIDTHS.split(',')
if ALLOWED_WIDTHS[0] == '':
    ALLOWED_WIDTHS = None
