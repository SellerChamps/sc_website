# frozen_string_literal: true

# HeyCatch reserved single-character paths (/a–/z, /0–/9) → homepage with campaign params.
# See https://heycatch.ai/agents.md step 4.
module Jekyll
  class HeycatchShortLinkGenerator < Generator
    safe true
    priority :lowest

    SHORT_LINK_CHARS = (("a".."z").to_a + (0..9).to_a.map(&:to_s)).freeze

    def generate(site)
      SHORT_LINK_CHARS.each do |code|
        from = "/#{code}/"
        to = "/?utm_source=heycatch&utm_campaign=#{code}"
        site.pages << JekyllRedirectFrom::RedirectPage.from_paths(site, from, to)
      end
    end
  end
end