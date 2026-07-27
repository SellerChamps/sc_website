# WordPress URL inventory (Phase 0)

Source: `wp-sitemap-posts-page-1.xml` + `wp-sitemap-posts-post-*.xml` (2026-07-23).
Raw lists: `_data/wp_pages.txt` (86), `_data/wp_posts.txt` (196).

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
| `/faq/` | rebuild |
| `/our-customers/` | rebuild |
| `/privacy/` | rebuild |
| `/terms-of-service/` | rebuild |
| `/blog/` + `/blog/{slug}/` | rebuild / migrate |
| `/support/` | rebuild (thin → KB/phone) |

## Keep (ads landings already in repo)
- `/ebay-lister-landing-v2/`
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
| `/terms-and-conditions/` | `/terms-of-service/` |
| `/always-in-touch-case-study/`, `/bonterra-companies-case-study/`, `/fragrance-spot-case-study/`, `/gamequest-case-study/` | `/our-customers/` |
| `/resources/`, `/amazon-fba-checklist/`, `/amazon-fba-revenue-calculator/`, `/ebay-fee-calculator/`, `/ebay-description/`, `/ecommerce-seo-checklist/`, `/free-shipping-label-template/`, `/shopify-store-checklist/`, `/updates/` | `/blog/` |
| `/landing-multi-channel-listing-software/`, `/landing-amazon-lister-multi-marketplace-listing-software/`, `/landing-fastest-ebay-lister-multi-marketplace-listing-software/`, `/sellerchamp-comparison-sellercloud/`, `/sellerchamp_comparison_sellercloud_rithum_landing/`, `/inkfrog-migration/` | `/landing-multi-channel-listing-software-v2/` |
| `/sellerchamp-affliate-program/`, `/partner-with-sellerchamp/`, `/prospershow/`, `/sellerchamp-carbon6-partnership/` | `/` |

## External (do not host)
- `app.sellerchamp.com` (login, signup, leads, contact)
- `kb.sellerchamp.com` (help docs)
- `community.sellerchamp.com`
