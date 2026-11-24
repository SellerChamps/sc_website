#!/usr/bin/env node
// Converts Ryze-published article JSON files into Jekyll posts in _posts/.
// No npm dependencies. Idempotent: re-running overwrites only its own output.

import { readdirSync, readFileSync, writeFileSync, existsSync, mkdirSync } from "node:fs";
import path from "node:path";

const RYZE_FOLDER = "blog/data";
const POSTS_DIR = "_posts";

function yamlEscape(str) {
  if (str === null || str === undefined) return "";
  return String(str).replace(/"/g, '\\"').replace(/\n/g, " ");
}

function loadArticles(dir) {
  if (!existsSync(dir)) return [];
  return readdirSync(dir)
    .filter((f) => f.endsWith(".json"))
    .map((f) => {
      const raw = readFileSync(path.join(dir, f), "utf8");
      try {
        return { file: f, data: JSON.parse(raw) };
      } catch (e) {
        console.error(`Skipping ${f}: invalid JSON (${e.message})`);
        return null;
      }
    })
    .filter(Boolean);
}

function dateOnly(isoString) {
  if (!isoString) return new Date().toISOString().slice(0, 10);
  return isoString.slice(0, 10);
}

function buildFrontMatter(article) {
  const title = yamlEscape(article.title || article.slug);
  const description = yamlEscape(article.meta_description || article.excerpt || "");
  const rawDate = article.published_at || article.updated_at || new Date().toISOString();
  // Strip fractional seconds (Jekyll's YAML date parser can choke on them)
  const dateStr = rawDate.replace(/\.\d+Z$/, "Z").replace("T", " ").replace("Z", " +0000");
  const lines = [
    "---",
    `title: "${title}"`,
    `date: ${dateStr}`,
    `permalink: /blog/${article.slug}/`,
    `description: "${description}"`,
    "reskin: true",
    "---",
    "",
  ];
  return lines.join("\n");
}

function buildBody(article) {
  const parts = [];

  // image is an object { url, alt } or null -- never interpolate the object itself
  if (article.image && article.image.url) {
    const alt = yamlEscape(article.image.alt || article.title || "");
    parts.push(`![${alt}](${article.image.url})`);
    parts.push("");
  }

  // body_html carries the fully rendered article (TL;DR, FAQ, stats, quote blocks).
  // Falls back to body_markdown if body_html is missing.
  const content = article.body_html || article.body_markdown || "";
  parts.push(content);

  return parts.join("\n");
}

function convert() {
  const articles = loadArticles(RYZE_FOLDER);
  if (!existsSync(POSTS_DIR)) mkdirSync(POSTS_DIR, { recursive: true });

  let written = 0;
  let skipped = 0;

  for (const { file, data: article } of articles) {
    if (!article.slug) {
      console.error(`Skipping ${file}: missing slug`);
      continue;
    }
    if (article.status !== "published") {
      skipped++;
      continue;
    }

    const dateStr = dateOnly(article.published_at || article.updated_at);
    const outFile = path.join(POSTS_DIR, `${dateStr}-${article.slug}.md`);
    const content = buildFrontMatter(article) + buildBody(article) + "\n";

    writeFileSync(outFile, content, "utf8");
    written++;
    console.log(`Wrote ${outFile}`);
  }

  console.log(`Ryze convert: ${written} post(s) written, ${skipped} skipped (not published).`);
}

convert();
