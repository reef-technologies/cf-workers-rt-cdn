# Cloudflare Workers CDN

CDN worker for Cloudflare Workers.

## Base requirements

* NodeJS
* Cloudflare Wrangler
* Transcrypt

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

1. Enable Cloudflare Workers Bundled plan.

**FoxTrap Workers setup:**

1. Go to the repository
1. Copy `wrangler.toml.template` to `wrangler.toml`

       cp wrangler.toml.template wrangler.toml

1. Set `account_id` and `zone_id` in `wrangler.toml`
    * You can find `account_id` and `zone_id` in the overview page of you site in the Cloudflare Dashboard
1. Set `route` and `vars` in `wrangler.toml`
    * You can set different environments (default are: `dev`, `staging` and `production`)
1. Set your Cloudflare API token:

       export CF_API_TOKEN=your_api_token

1. Publish the worker:
    * For `dev` environment:

          wrangler publish

    * For `staging` environment:

          wrangler publish --env=staging

    * For `production` environment:

          wrangler publish --env=production
