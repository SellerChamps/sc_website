# SellerChamp AEO / SEO plan (`sc_website` → sellerchamp.com)

**Owner:** Growth  
**Last updated:** 2026-11-17 (Phase 1 starter)  
**Living doc:** Notion (search “SellerChamp AEO SEO Plan”)

## Baseline (HubSpot AEO, 2026-10-18 → 2026-11-17)

| Metric | Value |
|--------|--------|
| Avg visibility (25 prompts) | 23.6% |
| Owned citation share | 313 / 5,904 (~5.3%) |
| Mention share vs competitors | SellerChamp ~13.7%; Sellbrite ~20.6%; Linnworks ~17.4% |
| Prompt capacity | 25 / 25 (full) |
| Strengths | Listing, cross-listing, liquidation/manifest, UPC bulk list, branded vs Sellbrite |
| Gaps | Repricer, PIM, Linnworks alternatives, generic inventory sync (0% visibility on several) |

## Site inventory (this repo)

- Tier 1 hubs, 9 feature URLs, ~30 integration pages, 6 ad landings, 202 blog posts
- Migration audit: 0 missing legacy URLs (`scripts/migration_audit.py`)
- Phase 0 shipped: `llms.txt`, `pricing.md`, `robots.txt`, FAQ schema on key pages, compare pages, AEO lead blocks

## Content pillars

1. **Multichannel listing & cross-listing** (primary revenue + AEO wins)
2. **Inventory sync & oversell prevention**
3. **Liquidation / high-volume reseller**
4. **Evaluation** (comparisons & alternatives)
5. **Integrations** (long-tail)

Calendar split: **60%** searchable · **30%** shareable · **10%** experimental.

## Phases

### Phase 0 (in progress)

- [x] Agent files: `llms.txt`, `pricing.md`, `robots.txt`
- [x] FAQ JSON-LD on `/pricing/`, `/bulk-lister-seller-champ/`, `/inventory-sync-software/`
- [x] AEO summary blocks (`aeo_lead`, `last_updated`) on those pages
- [x] Compare pages: `/compare/sellerchamp-vs-sellbrite/`, `/compare/sellerchamp-vs-sellercloud/` + redirects
- [x] Fix legacy comparison URLs in key landings
- [x] Footer + nav links to Compare and guides
- [ ] HubSpot: prompt swap (Nizar → HubSpot manager: delete 5, add 2 SellerCloud prompts)

### Phase 1 (months 1–3)

- [x] Listing + inventory hubs: `/guides/multichannel-listing-software/`, `/guides/inventory-sync-software/`
- [x] Compare hub `/compare/` + Linnworks compare
- [x] Listing Mirror compare: `/compare/sellerchamp-vs-listing-mirror/`
- Consolidate top blog posts → canonical product/compare URLs
- Repricer strategy: narrow FAQ vs full pillar

### Phase 2–4

See Notion doc for full backlog, KPIs, and distribution playbook.

## Phase 0 KPIs (90 days post-cutover)

- Owned citation share **>10%**
- Visibility **>40%** on core listing prompts
- Competitor Comparison campaign landing on `/compare/*`
- GSC: baseline impressions/clicks for money URLs (see [`GSC_POST_CUTOVER.md`](GSC_POST_CUTOVER.md))

## Related

- `.agents/product-marketing.md`
- `_data/url_inventory.md`
- `docs/SITE_MIGRATION.md`