# WordPress URL inventory (Phase 0)

Source: live `page-sitemap.xml` + `post-sitemap.xml` (refreshed 2026-11-17).
Raw lists: `_data/wp_pages.txt` (88), `_data/wp_posts.txt` (202).
`python3 scripts/migration_audit.py` — **0 missing pages, 0 missing posts** (repo inventory vs live sitemap lists).

## Classification legend
- **rebuild** — new page in this repo
- **redirect** — 301 via `jekyll-redirect-from` to a rebuild destination
- **keep** — already exists as ads landing in `landing/`
- **external** — stay off this site
- **retire** — no dedicated page; redirect to nearest hub

## Rebuild (Tier 1)
| Old / new path | Status |
|---|---|
| `/` | rebuild (homepage) |
| `/features/` | rebuild |
| `/pricing/` | rebuild (canonical) |
| `/integrations/` | rebuild |
| `/solutions/` | rebuild hub |
| `/solutions/ecommerce-reseller/` | rebuild |
| `/solutions/dropshipping-automation-software/` | rebuild |
| `/solutions/brand-owner/` | rebuild |
| `/solutions/retail-ecommerce-solution/` | rebuild |
| `/solutions/amazon-seller-software-for-fba/` | rebuild |
| `/solutions/walmart-listing-software/` | rebuild |
| `/faq/` | rebuild |
| `/our-customers/` | rebuild |
| `/privacy/` | rebuild |
| `/terms-of-service/` | rebuild |
| `/blog/` + `/blog/{slug}/` | rebuild / migrate |
| `/support/` | rebuild (thin → KB/phone) |

## Keep (ads landings already in repo)
- `/ebay-lister-landing-v2/`
- `/landing-amazon-lister-multi-marketplace-listing-software/`
- `/landing-multi-channel-listing-software-v2/`
- `/fullsuite-landing/`
- `/multichannel-operations/`

## Redirect map (implemented on destination front matter)
| From | To |
|---|---|
| `/home-3/`, `/landing/` | `/` |
| `/pricing-fullsuite-v2/`, `/pricing-fullsuite-v3/`, `/full-suite/`, `/full-suite/pricing-comparison/`, `/free-trial/` | `/pricing/` |
| `/bulk-lister-seller-champ/`, `/bulk-lister/`, `/bulk-lister/pricing-comparison/`, `/inventory-sync-software/`, `/multi-channel-fulfillment-software/`, `/repricer-software/`, `/repricer/`, `/repricer/pricing-comparison/`, `/ecommerce-analytics-tool-insights-reports/`, `/inventory-management-api-ftp/`, `/features/RePricer/` | `/features/` |
| `/integrations/market-places/`, `/integrations/market-places/*`, `/integrations/shopping-carts/`, `/integrations/shopping-carts/*`, `/integrations/service-integrations/`, `/integrations/service-integrations/*` | `/integrations/` |
| `/solutions/automotive-fitment-tool/`, `/solutions/e-commerce-inventory-forecasting-tool/`, `/solutions/e-commerce-shipping-integrations/`, `/solutions/ebay-lister/`, `/solutions/order-management-system-ecommerce/`, `/solutions/product-catalog-management/`, `/solutions/resellerold/` | `/solutions/` |
| `/terms-and-conditions/` | own page (Affiliate Agreement) |
| `/always-in-touch-case-study/`, `/bonterra-companies-case-study/`, `/fragrance-spot-case-study/`, `/gamequest-case-study/` | `/our-customers/` |
| `/resources/`, `/amazon-fba-revenue-calculator/`, `/ebay-fee-calculator/`, `/free-shipping-label-template/`, `/shopify-store-checklist/`, `/updates/` | `/blog/` |
| `/amazon-fba-checklist/`, `/ebay-description/`, `/ecommerce-seo-checklist/` | rebuild (see `pages/*-checklist*.html`, `pages/ebay-description.html`) |
| `/landing-multi-channel-listing-software/`, `/landing-fastest-ebay-lister-multi-marketplace-listing-software/`, `/sellerchamp-comparison-sellercloud/`, `/sellerchamp_comparison_sellercloud_rithum_landing/`, `/inkfrog-migration/` | `/landing-multi-channel-listing-software-v2/` |
| `/landing-amazon-lister-multi-marketplace-listing-software/` | dedicated Amazon Lister landing (no longer redirected) |
| `/sellerchamp-affliate-program/`, `/partner-with-sellerchamp/`, `/prospershow/`, `/sellerchamp-carbon6-partnership/` | `/` |

## External (do not host)
- `app.sellerchamp.com` (login, signup, leads, contact)
- `kb.sellerchamp.com` (help docs)
- `community.sellerchamp.com`
