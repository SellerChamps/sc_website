# SellerChamp AEO / SEO plan (`sc_website` → sellerchamp.com)

**Owner:** Growth  
**Last updated:** 2026-11-17 (Phase 1 batch)  
**Living doc:** Notion (search “SellerChamp AEO SEO Plan”)

## Baseline (HubSpot AEO, 2026-10-18 → 2026-11-17)

| Metric | Value |
|--------|--------|
| Avg visibility (23 prompts post-swap) | ~29.6% |
| Owned citation share | 313 / 5,904 (~5.3%) at pre-swap baseline |
| Mention share vs competitors | SellerChamp ~13.7%; Sellbrite ~20.6%; Linnworks ~17.4% |
| Prompt capacity | 23 active after Nov 2026 swap (was 25/25) |
| Strengths | Listing, cross-listing, liquidation/manifest, UPC bulk list, branded vs Sellbrite |
| Gaps | PIM (monitor), some generic prompts; repricer and inventory sync strengthened on-site Nov 2026 |

## Site inventory (this repo)

- Tier 1 hubs, 9 feature URLs, ~30 integration pages, 6 ad landings, 202 blog posts
- Migration audit: 0 missing legacy URLs (`scripts/migration_audit.py`)
- Agent files: `llms.txt`, `pricing.md`, `robots.txt`, FAQ schema on key pages, compare pages, AEO lead blocks

## Content pillars

1. **Multichannel listing & cross-listing** (primary revenue + AEO wins)
2. **Inventory sync & oversell prevention**
3. **Liquidation / high-volume reseller**
4. **Evaluation** (comparisons & alternatives)
5. **Integrations** (long-tail)

Calendar split: **60%** searchable · **30%** shareable · **10%** experimental.

## Phases

### Phase 0

- [x] Agent files: `llms.txt`, `pricing.md`, `robots.txt`
- [x] FAQ JSON-LD on `/pricing/`, `/bulk-lister-seller-champ/`, `/inventory-sync-software/`
- [x] AEO summary blocks (`aeo_lead`, `last_updated`) on key money pages
- [x] Compare pages + redirects (Sellbrite, SellerCloud, Rithum, Linnworks, Listing Mirror)
- [x] Fix legacy comparison URLs in key landings
- [x] Footer + nav links to Compare and guides
- [x] HubSpot: prompt swap (5 deletes, SellerCloud-oriented adds; manager completed Nov 2026)

### Phase 1 (months 1–3)

- [x] Listing + inventory hubs: `/guides/multichannel-listing-software/`, `/guides/inventory-sync-software/`
- [x] Compare hub `/compare/` + all current competitor pages (incl. Rithum)
- [x] Blog compare callouts → canonical `/compare/*` (Sellbrite, SellerCloud, ChannelAdvisor posts)
- [x] Repricer AEO: `aeo_lead` + `faq_schema` on `/repricer-software/`
- [x] Inventory / Linnworks AEO: expanded `faq_schema`, guide section, compare FAQs
- [x] `llms.txt` + `pricing.md` list all compare URLs
- [ ] Google Ads Competitor Comparison final URLs → `/compare/*` (needs Nizar approval)
- [ ] Monitor HubSpot for repricer / Linnworks / inventory sync prompt lift (30–60 days)
- [ ] PIM prompt strategy (narrow answer or defer)

### Phase 2–4

See Notion doc for full backlog, KPIs, and distribution playbook.

## Compare URL map (canonical)

| URL | Blog callout |
|-----|----------------|
| `/compare/sellerchamp-vs-sellbrite/` | `/blog/sellbrite-vs-sellerchamp/` |
| `/compare/sellerchamp-vs-sellercloud/` | `/blog/sellerchamp-vs-sellercloud/` |
| `/compare/sellerchamp-vs-rithum/` | `/blog/sellerchamp-vs-channeladvisor-comparison/` |
| `/compare/sellerchamp-vs-linnworks/` | (guide + feature page; no dedicated legacy blog) |
| `/compare/sellerchamp-vs-listing-mirror/` | — |

## Phase 0 KPIs (90 days post-cutover)

- Owned citation share **>10%**
- Visibility **>40%** on core listing prompts
- Competitor Comparison campaign landing on `/compare/*`
- GSC: baseline impressions/clicks for money URLs (see [`GSC_POST_CUTOVER.md`](GSC_POST_CUTOVER.md))

## Related

- `.agents/product-marketing.md`
- `_data/url_inventory.md`
- `docs/SITE_MIGRATION.md`