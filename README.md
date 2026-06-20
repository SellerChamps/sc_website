# SellerChamp Frontend - Built on Jekyll

Static rebuild of the SellerChamp.com website

## Run locally
```bash
bundle install
bundle exec jekyll serve --livereload
# → http://localhost:4000/ebay-lister-landing-v2/
```

## Deploy (GitHub Pages)

Pushes to `main` deploy via GitHub Actions.

- **Site URL:** https://sellerchamps.github.io/sc_website/
- **Landing page:** https://sellerchamps.github.io/sc_website/ebay-lister-landing-v2/

To publish: push to `main`. Monitor the **Deploy Jekyll site to Pages** workflow in the repo Actions tab.

- `_config.yml` — site + brand config (phone, app URLs, SEO)
- `_layouts/landing.html` — HTML shell, `<head>`, SEO meta, asset links
- `ebay-lister-landing-v2.html` — the page (front matter + sections)
- `assets/css/landing.css` — all styles, brand tokens at top
- `assets/js/landing.js` — pricing toggle + mobile nav
- `assets/images/` — drop real images here (see placeholders in the page)

## Images to add
Search the page for `.ph` placeholder blocks. The main one is the hero
(`hero-barcode.jpg`). Marketplace/partner/review badges are rendered as
styled text — swap to real logo `<img>` tags if you prefer.
