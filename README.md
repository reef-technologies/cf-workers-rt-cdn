# Cloudflare Workers CDN

CDN worker for Cloudflare Workers.

## Base requirements

* NodeJS
* Cloudflare Wrangler
* Transcrypt
* gettext

For a fresh ubuntu you can install the above with:
```
bash <(curl -sL https://deb.nodesource.com/setup_14.x)
apt install nodejs
npm i @cloudflare/wrangler -g --unsafe-perm=true --allow-root
pip install --user transcrypt
```

## Deployment

**Cloudflare Account setup:**

1. Create an [API key](https://support.cloudflare.com/hc/en-us/articles/200167836-Managing-API-Tokens-and-Keys) for your account with at least below permissions. You can use *Edit Cloudflare Workers* template.
    * Account.Workers KV Storage
    * Account.Workers Scripts
    * Account.Account Settings
    * User.User Details
    * Zone.Workers Routes

1. Enable Cloudflare Workers Bundled plan if you need.

**Cloudflare Worker setup:**

1. Go to the repository
1. Copy `.env.template` to `.env` and set your configuration there

       cp .env.template .env

1. Publish the worker (the .env must loaded by your shell):

       envsubst < wrangler.toml.template > wrangler.toml
       wrangler publish
