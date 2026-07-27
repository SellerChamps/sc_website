# SellerChamp website (Jekyll → GitHub Pages)

Static rebuild of [sellerchamp.com](https://sellerchamp.com) with the navy/teal design system from the multichannel operations landing pages.

## Run locally
```bash
bundle install
bundle exec jekyll serve --livereload
# → http://localhost:4000/
```

## Deploy
Pushes to `main` deploy via GitHub Actions (**Deploy Jekyll site to Pages**).

- Preview: `https://sellerchamps.github.io/sc_website/`
- Production cutover: see [`docs/CUTOVER.md`](docs/CUTOVER.md)

## Structure
| Path | Purpose |
|------|---------|
| `_layouts/default.html` | Site chrome (util bar, nav, CTA, footer) |
| `_layouts/page.html` / `post.html` | Marketing pages + blog posts |
| `_includes/` | Shared nav, footer, CTA, tracking |
| `pages/` | Features, pricing, integrations, solutions, FAQ, legal |
| `blog/` | Blog index |
| `_posts/` | Migrated WordPress posts (`/blog/{slug}/`) |
| `landing/` | Paid ads landings (unchanged permalinks) |
| `assets/css/site.css` | Site extensions on top of `multichannel_landing.css` |
| `_data/url_inventory.md` | WP URL rebuild/redirect map |
| `scripts/migrate_wp_blog.py` | Re-run blog import from live WP URLs |

## Blog re-import
```bash
python3 scripts/migrate_wp_blog.py
```

NOTE: Keep this repo public so GitHub Pages stays live. Keep `app`, `kb`, and `community` subdomains on their existing hosts.
