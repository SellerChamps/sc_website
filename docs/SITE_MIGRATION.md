# Site migration charter

**North star:** This repo replaces the current **sellerchamp.com** marketing site. When migration is done, **no public URL on sellerchamp.com should 404** because of the cutover. Every link that today resolves on sellerchamp.com must either exist in this project or redirect to a page that does.

## Hosting timeline

| Stage | Host | Role |
| --- | --- | --- |
| **Now** | [site.sellerchamp.com](https://site.sellerchamp.com) | Staging / preview of this Jekyll site |
| **After migration** | sellerchamp.com | Production DNS points at this repo (GitHub Pages) |

Do not cut over DNS until content parity and redirect coverage are verified on `site.sellerchamp.com`.

## What “done” means

1. **Move content** from the live WordPress site into this repo (pages, posts, landings, metadata) — **not** by blind copy/paste from WordPress HTML.
2. **Rewrite and reformat** — carry forward facts, structure, and SEO intent; rewrite copy and rebuild markup so it matches this site’s design system and reads fresh. Link integrity is still non‑negotiable (see below).
3. **Preserve URLs** — same path when possible; otherwise explicit **301** redirects (`jekyll-redirect-from` or equivalent). Track sources in `_data/url_inventory.md`.
4. **No broken links** — crawlers and bookmarks that hit `https://sellerchamp.com/...` must get a 200 on the right page or a 301 to it.
5. **External subdomains unchanged** — `app.`, `kb.`, `community.`, and other product hosts stay on their current targets (see `url_inventory` “External”).

## Content and design standards (migration)

WordPress/Elementor output does **not** ship as-is. For each page or post:

1. **Extract** meaning — headlines, benefits, facts, CTAs, internal links, target keywords — from the legacy page.
2. **Rewrite** using project skills:
   - Voice: `~/.cursor/skills/simple-english/SKILL.md` (**The Document** for pages; Plain mode for ads-style blocks). No em dash (—): `.cursor/rules/no-em-dash.mdc`.
   - Positioning: `.agents/product-marketing.md`.
   - Copy / CRO / SEO as needed: skills under `.cursor/skills/head-of-growth/marketingskills/` (e.g. `copywriting`, `copy-editing`, `seo-audit`, `cro`, `launch`).
3. **Rebuild HTML** with this repo’s patterns — layout, classes, components — not legacy inline styles or Elementor classes.
   - Marketing pages: `_layouts/page.html` + front matter (`hero_title`, `hero_sub`, `eyebrow`, sections in content).
   - Blog: `_layouts/post.html`; strip `elementor-*`, `fusion-*`, and WP wrapper markup from migrated bodies over time.
   - Paid landings: existing `_layouts/*_landing.html` and `landing/` patterns.
4. **Match the design system** — navy/teal palette, Montserrat/Inter (see `assets/css/site.css`, `assets/css/multichannel_landing.css`, `assets/css/fonts.css`). Reuse `_includes/` (nav, footer, CTA, feature blocks) and existing section class names from sibling pages before inventing new CSS.
5. **Refresh the feel** — shorter paragraphs, clear subheads, scannable lists, one primary CTA per section. Same information architecture intent; copy should look and read like the new site, not a theme swap.

If legacy and new markup must coexist briefly (e.g. blog import), plan a follow-up pass to rewrite and re-skin; do not treat raw import HTML as finished.

## Working rules for agents

- Treat **link preservation** as a release blocker, not a nice-to-have.
- Treat **design/copy parity with the new site** as required for every migrated page — no dump-and-ship WordPress HTML.
- When adding or editing a page, check inbound links from migrated blog HTML, nav, footer, and legacy WP paths.
- Prefer **rebuild + redirect** over leaving orphan URLs.
- Cutover steps: [`docs/CUTOVER.md`](CUTOVER.md).
- URL classification and redirect map: [`_data/url_inventory.md`](../_data/url_inventory.md).
- Live progress checklist: [`docs/MIGRATION_STATUS.md`](MIGRATION_STATUS.md). Audit: `python3 scripts/migration_audit.py`.

## Out of scope for “replace sellerchamp.com”

- Product app (`app.sellerchamp.com`), knowledge base (`kb.sellerchamp.com`), community — link to them; do not host them here unless explicitly planned.