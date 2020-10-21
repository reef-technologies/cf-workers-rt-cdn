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
