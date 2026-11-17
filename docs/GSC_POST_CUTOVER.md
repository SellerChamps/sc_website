# Google Search Console — post-cutover checklist

Use this **after** sellerchamp.com DNS points at this Jekyll site (not only `site.sellerchamp.com`).

## Week 1 (stability)

1. **Property** — Confirm GSC has the correct `https://sellerchamp.com` property (domain or URL-prefix).
2. **Sitemap** — Submit `https://sellerchamp.com/sitemap.xml`; confirm indexed URL count trends up, not down.
3. **Pages → Indexing** — Fix any spike in “Excluded” or “Not found (404)”. Cross-check `_data/url_inventory.md` redirects.
4. **Redirects** — Spot-check top legacy paths from WordPress (pricing, bulk-lister, comparison URLs, blog permalinks).
5. **Manual checks** — Home, `/pricing/`, `/bulk-lister-seller-champ/`, `/inventory-sync-software/`, `/compare/*`, `/faq/`.

## Week 2–4 (performance)

6. **Performance report** — Export last 28 days: queries with **impressions**, **average position**, **CTR**.
7. **Position 8–20** — Filter or sort for queries where you rank roughly 8–20. Those URLs are the fastest SEO wins (title, meta, `aeo_lead`, internal links, FAQ).
8. **Core Web Vitals** — Open CWV report; fix “Poor” on templates that drive demos (home, pricing, top feature pages).
9. **Compare / guide URLs** — Confirm `/compare/` and `/guides/*` gain impressions for “vs” and “what is” queries.

## Monthly (ongoing)

10. Re-run `python3 scripts/migration_audit.py` before marketing releases.
11. HubSpot AEO: review visibility on listing, inventory, and compare prompts after content ships.
12. Refresh `last_updated` and stats on compare pages when pricing or product facts change.

## Not in GSC

- **AI citation rate** — Use HubSpot AEO or manual checks on ChatGPT / Perplexity.
- **Paid conversion** — Google Ads + GA4, not Search Console.