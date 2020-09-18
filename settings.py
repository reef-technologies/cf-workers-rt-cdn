######################################################################
#
# File: settings.py
#
# Cloudflare Worker CDN
#
# Copyright (c) 2020, Reef Technologies. All Rights Reserved.
#
######################################################################

from dataclasses import dataclass


@dataclass(frozen=True)
class _Config:
    CDN_ALLOWED_HOSTS = JSON.parse(CDN_ALLOWED_HOSTS)

    # Below settings are fetched from wrangler.toml
    CDN_PREFIX = CDN_PREFIX


config = _Config()
