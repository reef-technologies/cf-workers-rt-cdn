######################################################################
#
# File: logger.py
#
# Cloudflare Worker CDN
#
# Copyright (c) 2020, Reef Technologies. All Rights Reserved.
#
######################################################################

import config


def debug(*args):
    if config.DEBUG:
        if config.ENV == 'dev':
            print(*args)
        else:
            console.log(*args)


def error(*args):
    if config.ENV == 'dev':
        print(*args)
    else:
        console.error(*args)
