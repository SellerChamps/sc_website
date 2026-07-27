# frozen_string_literal: true
# Encoding: UTF-8
# One-off generator: ruby scripts/generate_integration_pages.rb

require "yaml"
require "fileutils"
require "pathname"

root = Pathname(__dir__).parent
data = YAML.load_file(root.join("_data/integrations.yml"))

cat_labels = {
  "marketplace" => "Marketplace integration",
  "cart" => "Shopping cart integration",
  "shipping" => "Shipping integration",
  "fulfillment" => "Fulfillment integration",
  "service" => "Service integration"
}
eyebrows = {
  "marketplace" => "Marketplace",
  "cart" => "Shopping cart",
  "shipping" => "Shipping",
  "fulfillment" => "Fulfillment",
  "service" => "Service"
}

def yq(s)
  return '""' if s.nil?

  s = s.to_s
  if s.match?(/[:\#\{\}\[\]\&\*\!\|>'"%@`]|^\s|\s$|\n/)
    '"' + s.gsub("\\", "\\\\").gsub('"', '\\"') + '"'
  else
    s
  end
end

out_files = []

data.each do |item|
  path = item["path"].sub(%r{/?$}, "/")
  rel = path.sub(%r{^/integrations/}, "").sub(%r{/$}, "")
  out = root.join("pages/integrations", "#{rel}.html")
  FileUtils.mkdir_p(out.dirname)

  lines = []
  lines << "---"
  lines << "layout: page"
  lines << "permalink: #{path}"
  lines << "title: #{yq(item['title'])}"
  lines << "description: >-"
  item["description"].to_s.strip.each_line { |l| lines << "  #{l.rstrip}" }
  lines << "canonical: #{item['canonical']}"
  lines << "eyebrow: #{eyebrows[item['category']]}"
  lines << "nav_section: integrations"
  lines << "integration_name: #{yq(item['name'])}"
  lines << "integration_category: #{item['category']}"
  lines << "category_label: #{yq(cat_labels[item['category']])}"
  lines << "hero_title: #{yq(item['hero_title'])}"
  lines << "hero_sub: #{yq(item['hero_sub'])}"
  lines << "hero_cta: Book a Free Demo \u2192"
  lines << "show_runway: true"
  lines << "logo: #{item['logo']}" if item["logo"]
  lines << "logo_fullcolor: true" if item["logo_fullcolor"]
  lines << "logo_text: #{yq(item['logo_text'])}" if item["logo_text"]
  if item["redirects"]&.any?
    lines << "redirect_from:"
    item["redirects"].each { |r| lines << "  - #{r}" }
  end
  lines << "highlights:"
  (item["highlights"] || []).each do |h|
    lines << "  - title: #{yq(h['title'])}"
    lines << "    text: #{yq(h['text'])}"
  end
  lines << "---"
  lines << ""
  lines << "{% include integration-detail.html %}"
  lines << ""

  File.write(out, lines.join("\n"))
  out_files << out.relative_path_from(root).to_s
end

categories = [
  {
    permalink: "/integrations/market-places/",
    file: "pages/integrations/market-places/index.html",
    title: "Marketplace Integrations",
    description: "SellerChamp marketplace integrations for Amazon, eBay, Walmart, Etsy, TikTok Shop, Temu, and more.",
    canonical: "https://sellerchamp.com/integrations/market-places/",
    hero_title: "Marketplace integrations",
    hero_sub: "List, sync inventory, and fulfill orders across the world's most active marketplaces from one catalog.",
    filter: ->(i) { i["category"] == "marketplace" }
  },
  {
    permalink: "/integrations/shopping-carts/",
    file: "pages/integrations/shopping-carts/index.html",
    title: "Shopping Cart Integrations",
    description: "Connect Shopify, WooCommerce, and BigCommerce to your multichannel catalog with SellerChamp.",
    canonical: "https://sellerchamp.com/integrations/shopping-carts/",
    hero_title: "Shopping cart integrations",
    hero_sub: "Keep your storefront inventory and orders in sync with every marketplace you sell on.",
    filter: ->(i) { i["category"] == "cart" }
  },
  {
    permalink: "/integrations/service-integrations/",
    file: "pages/integrations/service-integrations/index.html",
    title: "Shipping, Fulfillment & Service Integrations",
    description: "ShipStation, ShipRush, Amazon FBA, Flexport, QuickBooks, Informed, and API & data feed integrations.",
    canonical: "https://sellerchamp.com/integrations/service-integrations/",
    hero_title: "Shipping, fulfillment & service integrations",
    hero_sub: "Connect fulfillment partners, shipping tools, accounting, and supplier feeds to the same ops platform.",
    filter: ->(i) { %w[shipping fulfillment service].include?(i["category"]) }
  }
]

categories.each do |cat|
  out = root.join(cat[:file])
  FileUtils.mkdir_p(out.dirname)
  items = data.select(&cat[:filter])

  cards = items.map do |i|
    logo_html = if i["logo"]
      fc = i["logo_fullcolor"] ? ' class="logo-fullcolor"' : ""
      "        <div class=\"int-detail-logo\"><img#{fc} src=\"{{ '#{i['logo']}' | relative_url }}\" alt=\"#{i['name']}\"></div>\n"
    elsif i["logo_text"]
      "        <div class=\"int-detail-logo int-detail-logo--text\"><span>#{i['logo_text']}</span></div>\n"
    else
      ""
    end
    <<~CARD
      <div class="rcard">
#{logo_html}        <h3><a href="{{ '#{i['path']}' | relative_url }}">#{i['name']}</a></h3>
        <p>#{i['hero_sub']}</p>
      </div>
    CARD
  end

  body = <<~HTML
    ---
    layout: page
    permalink: #{cat[:permalink]}
    title: #{yq(cat[:title])}
    description: >-
      #{cat[:description]}
    canonical: #{cat[:canonical]}
    eyebrow: Integrations
    nav_section: integrations
    hero_title: #{yq(cat[:hero_title])}
    hero_sub: #{yq(cat[:hero_sub])}
    hero_cta: Book a Free Demo \u2192
    show_runway: true
    ---

    <section class="site-section">
      <div class="wrap">
        <div class="slabel">Browse</div>
        <h2>#{cat[:title]}</h2>
        <span class="h2-line"></span>
        <p class="section-lead"><a href="{{ '/integrations/' | relative_url }}">&larr; All integrations</a></p>
        <div class="rgrid" style="margin-top:1.5rem;">
    #{cards.join}
        </div>
      </div>
    </section>
  HTML

  File.write(out, body)
  out_files << out.relative_path_from(root).to_s
end

puts "Wrote #{out_files.size} files"
puts out_files
