# DNS / GitHub Pages cutover checklist

Use this when Tier 1 pages + blog migration look good on the GitHub Pages preview URL.

## 1. GitHub Pages custom domain
1. Repo **Settings → Pages → Custom domain**: `sellerchamp.com`
2. Enable **Enforce HTTPS** after DNS propagates
3. Confirm `CNAME` file in repo root contains `sellerchamp.com` (already added)

## 2. Cloudflare DNS (sellerchamp.com)
Point apex + www to GitHub Pages per current GitHub docs:

- **Apex `sellerchamp.com`**: GitHub Pages A records (or Cloudflare CNAME flattening to `<org>.github.io`)
- **`www`**: CNAME → `<org>.github.io`

Keep `app`, `kb`, `community`, and other product subdomains on their current targets.

## 3. Baseurl
- Preview on `*.github.io/sc_website/` may use a project `baseurl`
- Custom domain cutover should use **empty** `baseurl` — confirm Actions `configure-pages` / `_config.yml` before flipping DNS

## 4. Redirects
- High-traffic WP URLs are wired via `redirect_from` on destination pages (see `_data/url_inventory.md`)
- After cutover, monitor Google Search Console **Coverage / 404s** for 2–4 weeks and add missing redirects

## 5. Cutover day
1. Freeze WP content edits
2. Final blog re-run: `python3 scripts/migrate_wp_blog.py`
3. Merge to `main`, confirm Pages deploy green
4. Switch Cloudflare DNS
5. Submit `https://sellerchamp.com/sitemap.xml` in Search Console
6. Keep WP Engine live ~2 weeks as emergency fallback, then decommission

## 7. Blog media (wp-content)
Migrated posts currently hotlink images from `https://sellerchamp.com/wp-content/...`.
**Before decommissioning WP Engine**, either:
- Keep a static mirror of `/wp-content/uploads/` on a CDN / object storage and leave URLs unchanged, or
- Re-run a media download pass and rewrite image paths to `/assets/images/blog/`

