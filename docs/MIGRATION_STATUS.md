# Migration status

Last updated: 2026-11-16. Re-run `python3 scripts/migration_audit.py` after large changes.

## Phase summary

| Phase | Goal | Status |
| --- | --- | --- |
| **A: URL parity** | Every WP page/post path returns 200 or 301 | **Done** (86 pages, 196 posts) |
| **B: Tier 1 pages** | Features, pricing, integrations, solutions, legal, case studies in new design | **In progress**. Solutions + Amazon/eBay/Walmart/Shopify depth done (2026-11-17); remaining integration YAML sections + blog rewrites next |
| **C: Blog reskin** | Replace Elementor import HTML with clean site styling | **Done (batch)**: `python3 scripts/reskin_all_posts.py`; manual exemplar: cycle counting post (`reskin: manual`) |
| **D: Media** | Blog images in `assets/images/blog/` | **Done**: `python3 scripts/migrate_blog_images.py` (448 files, ~57MB); 1 legacy 404 left on July 2024 update post |
| **E: Link crawl** | Internal links in blog/HTML point to repo paths, not dead WP URLs | **Not started** |
| **F: Cutover** | DNS → GitHub Pages, Search Console, monitoring | **Blocked** on B–E signoff — [`CUTOVER.md`](CUTOVER.md) |

## What to work on next (recommended order)

1. **Blog rewrite batches** — priority: high-traffic `/blog/*` from Search Console; use one reskinned post as template (`_posts/2024-09-23-what-is-cycle-counting-in-inventory-management.md`).
2. **Legacy blog CSS** — `assets/css/site.css` (`.post-body--legacy`) until each post is rebuilt.
3. **New landings** — e.g. `/multichannel-listing-tool/` (staging-only until live WP has URL or redirect plan).
4. **Refresh `_data/url_inventory.md`** — integration subpages are rebuilt pages, not hub redirects.
5. **Media migration** — before WP Engine shutdown.

## Commands

```bash
python3 scripts/migration_audit.py
bundle exec jekyll build && bundle exec jekyll serve
python3 scripts/migrate_wp_blog.py   # re-pull from live WP; then reskin, do not stop at import
```